from django.db import models
from django.db.models import Q
from mptt.models import MPTTModel, TreeForeignKey

class Specialization(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  name = models.CharField(max_length=255)


class NonCourseRequirement(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  year = models.PositiveSmallIntegerField()
  description = models.TextField()
  checklist = models.ForeignKey(
    'Checklist',
    on_delete=models.CASCADE,
    related_name='non_course_requirements'
  )


class AdditionalConstraint(MPTTModel):
  NODE_TYPES = [
    ('group', 'Group'),
    ('checkbox', 'Checkbox'),
  ]

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  title = models.CharField(max_length=64, blank=True, null=True)
  requirement_type = models.CharField(max_length=8, choices=NODE_TYPES)
  num_courses_required = models.PositiveSmallIntegerField(blank=True, null=True)
  target_checklist = models.ForeignKey(
    'Checklist',
    on_delete=models.CASCADE,
    related_name='additional_constraints'
  )
  parent = TreeForeignKey(
    'self',
    blank=True,
    null=True,
    on_delete=models.CASCADE,
    related_name='children'
  )

  class Meta:
    constraints = [
      models.CheckConstraint(
        check=(
          (~Q(requirement_type='group') &
           Q(num_courses_required__isnull=True))
           |
          (Q(requirement_type='group') &
           Q(num_courses_required__isnull=False))
        ),
        name='only_group_has_courses_required'
      )
    ]


class AdditionalConstraintAllowedCourses(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  target_checkbox = models.ForeignKey(
    'AdditionalConstraint',
    on_delete=models.CASCADE,
    related_name='allowed_courses'
  )
  courses = models.ManyToManyField(
    'courses.Course',
    related_name='+',
  )