from django.core.management.base import BaseCommand
from django.db import transaction
import json

from courses.models import Course, CoursePrerequisiteNode
from courses.services.uwflow_client.program_data import fetch_all_program_codes
from courses.services.uwflow_client.courses_data import fetch_all_courses_data
from courses.services.uw_web_scraper.courses_data import scrape_courses
from courses.services.openai_client.course_data import parse_prereqs

sample_json_data = [
  {
    'code': 'CS',
    'number': '115',
    'units': 10,
    'category': ['cs', 'math'],
    'title': 'racket',
    'description': 'learn easier functions',
    'num_uwflow_ratings': 100,
    'uwflow_liked_rating': 60,
    'uwflow_easy_ratings': 30,
    'uwflow_useful_ratings': 90,

    'prereqs': '0()',
    'coreqs': [],
    'antireqs': [],
  },
  {
    'code': 'CS',
    'number': '116',
    'units': 10,
    'category': ['cs', 'math'],
    'title': 'python',
    'description': 'learn ds with python',
    'num_uwflow_ratings': 100,
    'uwflow_liked_rating': 60,
    'uwflow_easy_ratings': 30,
    'uwflow_useful_ratings': 90,

    'prereqs': '1(CS_115)',
    'coreqs': [],
    'antireqs': [],
  },
  {
    'code': 'CS',
    'number': '145',
    'units': 10,
    'category': ['cs', 'math'],
    'title': 'racket',
    'description': 'learn functions',
    'num_uwflow_ratings': 100,
    'uwflow_liked_rating': 60,
    'uwflow_easy_ratings': 30,
    'uwflow_useful_ratings': 90,

    'prereqs': '0()',
    'coreqs': [],
    'antireqs': [],
  },
  {
    'code': 'CS',
    'number': '135',
    'units': 10,
    'category': ['cs', 'math'],
    'title': 'racket',
    'description': 'learn functional programming',
    'num_uwflow_ratings': 100,
    'uwflow_liked_rating': 60,
    'uwflow_easy_ratings': 30,
    'uwflow_useful_ratings': 90,

    'prereqs': '0()',
    'coreqs': [],
    'antireqs': [],
  },
  {
    'code': 'CS',
    'number': '136',
    'units': 10,
    'category': ['cs', 'math'],
    'title': 'C',
    'description': 'learn ds with c',
    'num_uwflow_ratings': 100,
    'uwflow_liked_rating': 60,
    'uwflow_easy_ratings': 30,
    'uwflow_useful_ratings': 90,

    'prereqs': '1(CS_135 cs_145 cs_116)',
    'coreqs': [],
    'antireqs': [],
  },
  {
    'code': 'CS',
    'number': '146',
    'units': 10,
    'category': ['cs', 'math'],
    'title': 'C',
    'description': 'learn ds with c',
    'num_uwflow_ratings': 100,
    'uwflow_liked_rating': 60,
    'uwflow_easy_ratings': 30,
    'uwflow_useful_ratings': 90,

    'prereqs': '1(CS_135 cs_145)',
    'coreqs': [],
    'antireqs': [],
  },
  {
    'code': 'CS',
    'number': '136L',
    'units': 10,
    'category': ['cs', 'math'],
    'title': 'bash',
    'description': 'learn terminal',
    'num_uwflow_ratings': 100,
    'uwflow_liked_rating': 60,
    'uwflow_easy_ratings': 30,
    'uwflow_useful_ratings': 90,

    'prereqs': '1(CS_135 CS_145)',
    'coreqs': [],
    'antireqs': [],
  },
  {
    'code': 'CS',
    'number': '138',
    'units': 10,
    'category': ['cs', 'math'],
    'title': 'C',
    'description': 'learn ds with c',
    'num_uwflow_ratings': 100,
    'uwflow_liked_rating': 60,
    'uwflow_easy_ratings': 30,
    'uwflow_useful_ratings': 90,

    'prereqs': '0()',
    'coreqs': [],
    'antireqs': [],
  },
  {
    'code': 'CS',
    'number': '246',
    'units': 5,
    'category': ['cs', 'math'],
    'title': 'OOP with C++',
    'description': 'learn oop with c++',
    'num_uwflow_ratings': 100,
    'uwflow_liked_rating': 60,
    'uwflow_easy_ratings': 30,
    'uwflow_useful_ratings': 90,

    'prereqs': '1(CS_138 2(CS_136L CS_146)2(CS_136L CS_136))',
    'coreqs': [],
    'antireqs': [],
  },
]


class Command(BaseCommand):
  help = "Fetch all undergrad course data and store them in the database" 

  @staticmethod
  def _update_courses_model(item: dict):
    # Convert coreqs and antireqs lists to combined code+number format (TODO Should i add spacing?)
    coreqs = [f"{code.upper()}_{num.upper()}" for code, num in item.get('coreqs', [])]
    antireqs = [f"{code.upper()}_{num.upper()}" for code, num in item.get('antireqs', [])]
    
    course, _ = Course.objects.update_or_create(
        code=item['code'].upper(),
        number=item['number'].upper(),
        defaults={
          'units': item['units'],
          'category': [c.lower() for c in item['category']],
          'corequisites': coreqs,
          'antirequisites': antireqs,
          'title': item['title'].title(),
          'description': item['description'],
          'num_uwflow_ratings': item['num_uwflow_ratings'],
          'uwflow_liked_rating': item['uwflow_liked_rating'],
          'uwflow_easy_ratings': item['uwflow_easy_ratings'],
          'uwflow_useful_ratings': item['uwflow_useful_ratings'],
        }
      )
    return course
    
  @staticmethod
  def _update_prerequisite_model(item: dict, target_course):
    Command._create_prerequisite_nodes(target_course, item['prereqs'])

  @transaction.atomic
  @staticmethod
  def _create_prerequisite_nodes(target_course, req_str: str='0()'):
    """
    Parse req_str into MPTT node structure.
    Sample input for CS246:
      target_course: id for CS246
      req_str: '1(CS_138 2(CS_136L CS_146)2(CS_136L CS_136))'
    """
    # Use context manager to temporarily disable mptt updates
    with CoursePrerequisiteNode.objects.disable_mptt_updates():
      # Clear tree
      CoursePrerequisiteNode.objects.filter(
        target_course=target_course,
      ).delete()

      number: str = ''
      course_code: str = ''
      parent_stack: list = [None]
      reading_course_num: bool = False

      for c in req_str:
        # Create group node
        if c == '(':
          parent = CoursePrerequisiteNode.objects.create(
            target_course=target_course,
            parent=parent_stack[-1],
            node_type='group',
            leaf_course=None,
            num_children_required=int(number),
          )

          number = ''
          parent_stack.append(parent)
        # Create leaf course
        elif c == ' ':
          leaf_course = Course.objects.get( # Assumes course exists
            code=course_code.upper(),
            number=number.upper()
          )
          CoursePrerequisiteNode.objects.create(
            target_course=target_course,
            parent=parent_stack[-1],
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
              code=course_code.upper(),
              number=number.upper()
            )
            CoursePrerequisiteNode.objects.create(
              target_course=target_course,
              parent=parent_stack[-1],
              node_type='course',
              leaf_course=leaf_course,
              num_children_required=None,
            )

          course_code = '' 
          number = ''
          reading_course_num = False
          parent_stack.pop()

    # After bulk changes, rebuild the tree fields
    CoursePrerequisiteNode.objects.rebuild()

  @staticmethod
  @transaction.atomic
  def _update_course(item):
    item['code'] = item['code'].upper()
    item['number'] = item['number'].upper()
    course = Command._update_courses_model(item)
    Command._update_prerequisite_model(item, course)

  @staticmethod
  def _filter_course_data(course_data1: list, course_data2: list):
    """
    course_data2 includes requisites and units, and course_data1 includes
    everything else.
    """
    data = dict()
    # Merge courses for each program
    for course1 in course_data1:
      if course1['code'] in data:
        data[course1['code']] = list()

      data[course1['code']].append(course1)
      # Find the same course in course_data2 and raise error if not found
      match_found = False
      for course2 in course_data2:
        if course2['code'] == course1['code'] and \
           course2['number'] == course1['number']:
          data[course1['code']]['units'] = course2['units']
          data[course1['code']]['prereqs'] = course2['prereqs']
          data[course1['code']]['antireqs'] = course2['antireqs']
          data[course1['code']]['coreqs'] = course2['coreqs']
          match_found = True
          break
      if not match_found:
        raise ValueError(
          f"{course1['code']}{course1['number']} is not in html calenders."
        )
          
        
    # Check for missing course in reverse direction
    for course2 in course_data2:
      match_found = False
      for course1 in course_data1:
        if course2['code'] == course1['code'] and \
           course2['number'] == course1['number']:
          match_found = True
          break
      if not match_found:
        raise ValueError(
          f"{course2['code']}{course2['number']} is not in uwflow query."
        )

    # Order courses in each program
    for _, courses in data.items():
      courses.sort(key=lambda course: course['number'])

    return data
    
  def handle(self, *args, **options):
    course_data1 = fetch_all_courses_data()
    with open('uw_course_reqs.json', 'r') as f:
      course_data2 = json.load(f)
    data = Command._filter_course_data(course_data1, course_data2)
    # Translate 

    with: open('finalized_data.json')

    for item in data:
      Command._update_course(item)
      
