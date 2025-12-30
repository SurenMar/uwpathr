from django.core.management.base import BaseCommand
from django.db import transaction
import json

from courses.models import Course, CoursePrerequisiteNode
from courses.services.uwflow_client.program_data import fetch_all_program_codes
from courses.services.uwflow_client.courses_data import fetch_all_courses_data
from courses.services.uw_web_scraper.courses_data import scrape_courses
from courses.utils.course_utils import split_full_code


class Command(BaseCommand):
  help = "Fetch all undergrad course data and store them in the database" 

  @staticmethod
  def _normalize_requisite_text(value):
    """Return a safe string for coreqs/antireqs TextFields."""
    if value is None:
      return ''
    if isinstance(value, str):
      return value.strip()
    if isinstance(value, (list, tuple)):
      formatted = []
      for item in value:
        if isinstance(item, (list, tuple)) and len(item) == 2:
          code, num = item
          formatted.append(f"{code}_{num}".upper())
        elif isinstance(item, str):
          formatted.append(item.strip())
      return ' '.join(formatted)
    return str(value)

  @staticmethod
  def _update_courses_model(item: dict):
    # Normalize coreqs and antireqs into plain text for TextFields
    #print('\tupdating course model')
    coreqs = Command._normalize_requisite_text(item.get('coreqs'))
    antireqs = Command._normalize_requisite_text(item.get('antireqs'))
    
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

  @transaction.atomic
  @staticmethod
  def _create_prerequisite_nodes(target_course, req_str: str):
    #print('\tcreating prereq nodes')
    if req_str == None:
      return
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
          if course_code and number:
            leaf_course = Course.objects.get(
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
          #print(f'\t\t{course_code}{number}')
          course_code = '' 
          number = ''
          reading_course_num = False
        # Read course
        elif c.isalpha() and not reading_course_num:
          course_code += c
        # Read course
        elif (c.isalpha() or c.isnumeric()) and reading_course_num:
          number += c
        # Read course number
        elif c.isnumeric() and course_code:
          reading_course_num = True
          number += c
        # Read num_children_required count
        elif c.isnumeric():
          number += c
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
          #print(f'\t\t{course_code}{number}')
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
    Command._create_prerequisite_nodes(course, item['prereqs'])

  @staticmethod
  def _filter_course_data(course_data1: list, course_data2: list):
    """
    course_data2 includes requisites and units, and course_data1 includes
    everything else.
    """
    data = dict()
    # Merge courses for each program
    for course1 in course_data1:
      # Append course only if it is also in course_data2
      for course2 in course_data2:
        if (course2['code'] == course1['code'] and \
            course2['number'] == course1['number']):
          if course1['code'] not in data:
            data[course1['code']] = list()
          data[course1['code']].append(course1)
          data[course1['code']][-1]['units'] = course2['units']
          data[course1['code']][-1]['prereqs'] = course2['prereqs']
          data[course1['code']][-1]['antireqs'] = course2['antireqs']
          data[course1['code']][-1]['coreqs'] = course2['coreqs']
          break
        
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

    prereqs = dict()
    # Override raw prerequisites with parsed
    with open('only_prereqs.json', 'r') as f:
      prereqs = json.load(f)

    for full_code, prereq in prereqs.items():
      code, number = split_full_code(full_code)
      for course in data[code]:
        if course['number'] == number:
          course['prereqs'] = prereq
          break

    return data
    
  def handle(self, *args, **options):
    # Simply read from this file now that it has been initialized
    with open('finalized_data.json', 'r') as f1:
      data = json.load(f1)

    with transaction.atomic():
      # Loop until every course has been added
      while data:
        for program, program_courses in list(data.items()):
          for course in list(program_courses):
            try:
              Command._update_course(course)
              data[program].remove(course)
              if not data[program]:
                del data[program]
            except Course.DoesNotExist:
              continue
      
