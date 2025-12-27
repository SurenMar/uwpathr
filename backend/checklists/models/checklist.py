from django.db import models
from django.db.models import Q
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


class ChecklistNode(MPTTModel):
  NODE_TYPES = [
    ('head', 'Head'),
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

  class Meta:
    constraints = [
      models.CheckConstraint(
        check=(
          (~Q(requirement_type='group') &
           Q(units_required__isnull=True))
           |
          (Q(requirement_type='group') &
           Q(units_required__isnull=False))
        ),
        name='only_group_has_units_required'
      )
    ]
  
  def target_year(self):
    return self.target_checklist.year

  def target_specialization(self):
    return self.target_checklist.specialization


class CheckboxAllowedCourses(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  target_checkbox = models.ForeignKey(
    'ChecklistNode',
    on_delete=models.CASCADE,
    related_name='allowed_courses'
  )
  courses = models.ManyToManyField(
    'courses.Course',
    related_name='+',
  )

  def target_requiremet_type(self):
    return self.target_checkbox.requirement_type
  
  def target_title(self):
    return self.target_checkbox.title
  
  def course_list(self):
    return ", ".join(str(i) for i in self.courses.all())
  course_list.short_description = "Courses"
