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

with transaction.atomic():
  for i in range(13, 16):
    foo = CheckboxAllowedCourses.objects.create(
      target_checkbox_id = i
    )
    foo.courses.add(*cs3xx)
    foo.courses.add(*cs4xx)

  for i in range(16, 18):
    foo = CheckboxAllowedCourses.objects.create(
      target_checkbox_id = i
    )
    foo.courses.add(*cs4xx)

  foo = CheckboxAllowedCourses.objects.create(
    target_checkbox_id = 18
  )
  co487 = Course.objects.get(code = 'CO', number = '487')
  stat440 = Course.objects.get(code = 'STAT', number = '440')
  cs499t = Course.objects.get(code = 'CS', number = '499T')
  foo.courses.add(*cs4xx, co487, stat440, cs499t)

  foo = CheckboxAllowedCourses.objects.create(
    target_checkbox_id = 29
  )
  foo.courses.add(*ss_course)
  foo = CheckboxAllowedCourses.objects.create(
    target_checkbox_id = 30
  )
  foo.courses.add(*ss_course)

  foo = CheckboxAllowedCourses.objects.create(
    target_checkbox_id = 31
  )
  foo.courses.add(*ps_course)

  foo = CheckboxAllowedCourses.objects.create(
    target_checkbox_id = 32
  )
  foo.courses.add(*ps_course, *as_course)

  foo = CheckboxAllowedCourses.objects.create(
    target_checkbox_id = 33
  )
  foo.courses.add(*non_math_course)

  foo = CheckboxAllowedCourses.objects.create(
    target_checkbox_id = 34
  )
  foo.courses.add(*non_math_course)

  for i in range(36, 44):
    foo = CheckboxAllowedCourses.objects.create(
      target_checkbox_id = i
    )
