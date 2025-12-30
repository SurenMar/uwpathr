import os
import django

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "core.settings"
)

django.setup()

from courses.models import Course
from checklists.models.checklist import CheckboxAllowedCourses
from django.db import transaction

courses = list(Course.objects.all())
cs3xx = []
cs4xx = []
hum_course = []
ss_course = []
as_course = []
ps_course = []
comm1_course = []
comm2_course = []
non_math_course = []
other = []


for course in courses:
  if course.code == 'CS':
    if course.number[0] == '3' and int(course.number[1]) >= 4 and course.number != '399':
      cs3xx.append(course)
    elif course.number[0] == '4' and int(course.number[1]) >= 4 and int(course.number[1]) <= 8:
      cs4xx.append(course)

  if 'hum' in course.category:
    hum_course.append(course)
  if 'ss' in course.category:
    ss_course.append(course)
  if 'as' in course.category:
    as_course.append(course)
  if 'ps' in course.category:
    ps_course.append(course)
  if 'comm1' in course.category:
    comm1_course.append(course)
  if 'comm2' in course.category:
    comm2_course.append(course)
  if 'non_math' in course.category:
    non_math_course.append(course)
  if (course.code == 'EMLS' and (course.number == '103R' or course.number == '104R' or course.number == '110R')) or \
     (course.code == 'MTHEL' and course.number == '300'):
    other.append(course)

with transaction.atomic():
  foo = CheckboxAllowedCourses.objects.create(
    target_checkbox_id = 49
  )
  foo.courses.add(*comm1_course)

  foo = CheckboxAllowedCourses.objects.create(
    target_checkbox_id = 50
  )
  foo.courses.add(*comm2_course)

  foo = CheckboxAllowedCourses.objects.create(
    target_checkbox_id = 51
  )
  foo.courses.add(*hum_course)

  foo = CheckboxAllowedCourses.objects.create(
    target_checkbox_id = 52
  )
  foo.courses.add(*hum_course)

  foo = CheckboxAllowedCourses.objects.create(
    target_checkbox_id = 54
  )
  foo.courses.add(*comm1_course)

  foo = CheckboxAllowedCourses.objects.create(
    target_checkbox_id = 55
  )
  result = [x for x in comm2_course if x not in other]
  foo.courses.add(*result)

  foo = CheckboxAllowedCourses.objects.create(
    target_checkbox_id = 56
  )
  foo.courses.add(*hum_course)

  foo = CheckboxAllowedCourses.objects.create(
    target_checkbox_id = 57
  )
  foo.courses.add(*non_math_course)
