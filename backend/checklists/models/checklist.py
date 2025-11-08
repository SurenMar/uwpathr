from django.db import models
from mptt.models import MPTTModel, TreeForeignKey


class Checklist(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  year = models.PositiveSmallIntegerField()
  units_required = models.PositiveSmallIntegerField()
  specialization = models.ForeignKey(
    'Specialization',
    on_delete=models.PROTECT,
    related_name='+'
  )


class ChecklistRequirementNode(MPTTModel):
  NODE_TYPES = [
    ('group', 'Group'),
    ('checkbox', 'Checkbox'),
  ]

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  requirement_type = models.CharField(max_length=8, choices=NODE_TYPES)
  title = models.CharField(max_length=64)
  units_required = models.PositiveSmallIntegerField(blank=True, null=True)
  target_checklist = models.ForeignKey(
    'Checklist',
    on_delete=models.CASCADE,
    related_name='nodes'
  )
  parent = TreeForeignKey(
    'self',
    blank=True,
    null=True,
    on_delete=models.CASCADE,
    related_name='children'
  )


class CheckboxAllowedCourses(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  target_checkbox = models.ForeignKey(
    'ChecklistRequirementNode',
    on_delete=models.CASCADE,
    related_name='allowed_courses'
  )
  courses = models.ManyToManyField(
    'courses.Course',
    related_name='+',
  )
  