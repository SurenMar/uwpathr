from django.db import models
from django.db.models import Q
from mptt.models import MPTTModel, TreeForeignKey


class UserChecklist(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  year = models.PositiveSmallIntegerField()
  user = models.OneToOneField(
    'users.UserAccount',
    on_delete=models.CASCADE,
    related_name='checklists'
  )
  units_required = models.PositiveSmallIntegerField()
  taken_course_units = models.PositiveSmallIntegerField(blank=True, default=0)
  planned_course_units = models.PositiveSmallIntegerField(blank=True, default=0)
  specialization = models.ForeignKey(
    'checklists.Specialization',
    on_delete=models.PROTECT,
    related_name='+'
  )
  # TODO Add indexing and ordering for frontend csr


class UserChecklistNode(MPTTModel):
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
  units_gathered = models.PositiveSmallIntegerField(blank=True, null=True)
  completed = models.BooleanField()
  user = models.OneToOneField(
    'users.UserAccount',
    on_delete=models.CASCADE,
    related_name='checklist_nodes'
  )
  target_checklist = models.ForeignKey(
    'UserChecklist',
    on_delete=models.CASCADE,
    related_name='nodes'
  )
  # Use this to access allowed courses
  original_checkbox = models.ForeignKey(
    'checklists.ChecklistNode',
    blank=True,
    null=True,
    on_delete=models.PROTECT,
    related_name='+'
  )
  parent = TreeForeignKey(
    'self',
    blank=True,
    null=True,
    on_delete=models.CASCADE,
    related_name='children'
  )

  class Meta:
    # TODO Add indexing and ordering for frontend csr
    constraints = [
      models.CheckConstraint(
        check=(
          (~Q(requirement_type='group') &
           Q(units_required__isnull=True) &
           Q(units_gathered__isnull=True))
           |
          (Q(requirement_type='group') &
           Q(units_required__isnull=False) &
           Q(units_gathered__isnull=False))
        )
      ),
      models.CheckConstraint(
        check=(
          (~Q(requirement_type='checkbox') &
           Q(original_checkbox__isnull=True))
           |
          (Q(requirement_type='checkbox') &
           Q(original_checkbox__isnull=True))
        )
      )
    ]


class UserAdditionalConstraint(MPTTModel):
  NODE_TYPES = [
    ('group', 'Group'),
    ('checkbox', 'Checkbox'),
  ]

  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  title = models.CharField(max_length=64, blank=True, null=True)
  requirement_type = models.CharField(max_length=8, choices=NODE_TYPES)
  num_courses_required = models.PositiveSmallIntegerField(blank=True, null=True)
  num_courses_gathered = models.PositiveSmallIntegerField(blank=True, null=True)
  completed = models.BooleanField()
  user = models.OneToOneField(
    'users.UserAccount',
    on_delete=models.CASCADE,
    related_name='checklist_nodes'
  )
  target_checklist = models.ForeignKey(
    'UserChecklist',
    on_delete=models.CASCADE,
    related_name='additional_constraints'
  )
  # Use this to access allowed courses
  original_checkbox = models.ForeignKey(
    'checklists.AdditionalConstraint',
    blank=True,
    null=True,
    on_delete=models.PROTECT,
    related_name='+'
  )
  parent = TreeForeignKey(
    'self',
    blank=True,
    null=True,
    on_delete=models.CASCADE,
    related_name='children'
  )

  class Meta:
    # TODO Add indexing and ordering for frontend csr
    constraints = [
      models.CheckConstraint(
        check=(
          (~Q(requirement_type='group') &
           Q(courses_required__isnull=True) &
           Q(courses_gathered__isnull=True))
           |
          (Q(requirement_type='group') &
           Q(courses_required__isnull=False) &
           Q(courses_gathered__isnull=False))
        )
      ),
      models.CheckConstraint(
        check=(
          (~Q(requirement_type='checkbox') &
           Q(original_checkbox__isnull=True))
           |
          (Q(requirement_type='checkbox') &
           Q(original_checkbox__isnull=True))
        )
      )
    ]


class UserDepthList(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  user = models.ForeignKey(
    'users.UserAccount',
    on_delete=models.CASCADE,
    related_name='depth_lists' # TODO We might not need this reverse relationship
  )
  courses = models.ManyToManyField(
    'progress.UserCourse', 
    related_name='depth_lists'
  )
  is_chain = models.BooleanField(blank=True, null=True)
  total_units = models.PositiveSmallIntegerField(blank=True, null=True)
  num_courses = models.PositiveSmallIntegerField(blank=True, null=True)

  class Meta:
    constraints = [
      models.CheckConstraint(
        check=(
          (Q(is_chain=True) & 
           Q(num_courses__isnull=False) & 
           Q(total_credits__isnull=True))
           |
          (Q(is_chain=False) & 
           Q(num_courses__isnull=True) & 
           Q(total_credits__isnull=False))
        )
      ),
    ]
