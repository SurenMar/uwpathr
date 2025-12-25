from django.core.management.base import BaseCommand
from django.db import transaction

from courses.models import Course, CourseRequisiteNode

sample_json_data = [
    {
        'code': 'CS',
        'number': '246',
        'units': 10,
        'offered_next_term': True,
        'category': ['cs', 'math'],
        'title': 'OOP with C++',
        'description': 'learn oop with c++',
        'num_uwflow_ratings': 100,
        'uwflow_liked_rating': 60,
        'uwflow_easy_ratings': 30,
        'uwflow_useful_ratings': 90,

        'pre': '1(CS_138 2(CS_136L CS_146)2(CS_136L CS_136))',
        'co': '0()',
        'anti': '0()',
    },
]

class Command(BaseCommand):
  help = "Fetch courses data and store them in the database" 

  def update_courses_model(self, item: dict):
    # TODO Manually add uwflow id so you can compare for course changes
    course, _ = Course.objects.update_or_create(
        code=item['code'].lower(),
        number=item['number'].lower(),
        defaults={
          'units': item['units'],
          'offered_next_term': item['offered_next_term'],
          'category': [c.lower() for c in item['category']],
          'title': item['title'].title(),
          'description': item['description'],
          'num_uwflow_ratings': item['num_uwflow_ratings'],
          'uwflow_liked_rating': item['uwflow_liked_rating'],
          'uwflow_easy_ratings': item['uwflow_easy_ratings'],
          'uwflow_useful_ratings': item['uwflow_useful_ratings'],
        }
      )
    return course
    
  def update_requisite_model(self, item: dict, target_course):
    self.create_req_nodes(target_course, 'pre', item['pre'])
    self.create_req_nodes(target_course, 'co', item['co'])
    self.create_req_nodes(target_course, 'anti', item['anti'])

  @transaction.atomic
  def create_req_nodes(self, target_course, req_type: str, 
    req_str: str='0()'):
    """
    Parse req_str into MPTT node structure.
    Sample input for CS246:
      target_course: id for CS246
      req_type: 'pre'
      req_str: '1(CS_138 2(CS_136L CS_146)2(CS_136L CS_136))'
    """
    CourseRequisiteNode.objects.disable_mptt_updates()
    
    try:
      # Clear tree
      CourseRequisiteNode.objects.filter(
        target_course=target_course,
        requisite_type=req_type,
      ).delete()

      number: str = ''
      course_code: str = ''
      parent_stack: list = [None]
      reading_course_num: bool = False

      for c in req_str:
        # Create group node
        if c == '(':
          parent = CourseRequisiteNode.objects.create(
            target_course=target_course,
            parent=parent_stack[-1],
            requisite_type=req_type,
            node_type='group',
            leaf_course=None,
            num_children_required=int(number),
          )

          number = ''
          parent_stack.append(parent)
        # Create leaf course
        elif c == ' ':
          leaf_course = Course.objects.get( # Assumes course exists
            code=course_code.lower(),
            number=number.lower()
          )
          CourseRequisiteNode.objects.create(
            target_course=target_course,
            parent=parent_stack[-1],
            requisite_type=req_type,
            node_type='course',
            leaf_course=leaf_course,
            num_children_required=None,
          )

          course_code = '' 
          number = ''
          reading_course_num = False
        # Read course
        elif c.isalpha() and not reading_course_num:
          course_code += c
        # Read course
        elif (c.isalpha() or c.isnumeric()) and reading_course_num:
          number += c
        # Read num_children_required count
        elif c.isnumeric():
          number += c
        # Switch to course number
        elif c == '_':
          reading_course_num = True
        # Create leaf course and pop current parent
        elif c == ')':
          if course_code and number:
            leaf_course = Course.objects.get( # Assumes course exists
              code=course_code.lower(),
              number=number.lower()
            )
            CourseRequisiteNode.objects.create(
              target_course=target_course,
              parent=parent_stack[-1],
              requisite_type=req_type,
              node_type='course',
              leaf_course=leaf_course,
              num_children_required=None,
            )

          course_code = '' 
          number = ''
          reading_course_num = False
          parent_stack.pop()

    finally:
      CourseRequisiteNode.objects.enable_mptt_updates()
      CourseRequisiteNode.objects.rebuild()

    
  def handle(self, *args, **options):
    data = sample_json_data

    for item in data:
      course = self.update_courses_model(item)
      self.update_requisite_model(item, course)
