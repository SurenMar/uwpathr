from django.db import models
from django.db.models import Q, Sum
from django.dispatch import receiver
from django.db.models.signals import m2m_changed, post_save, pre_delete
from mptt.models import MPTTModel, TreeForeignKey


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
  completed = models.BooleanField(default=False)
  user = models.ForeignKey(
    'users.UserAccount',
    on_delete=models.CASCADE,
    related_name='additional_contraints'
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
          (Q(requirement_type='checkbox') &
           Q(num_courses_required__isnull=True) &
           Q(num_courses_gathered__isnull=True))
           |
          (Q(requirement_type='group') &
           Q(num_courses_required__isnull=False) &
           Q(num_courses_gathered__isnull=False))
        ),
        name='only_groups_have_courses'
      ),
      models.CheckConstraint(
        check=(
          (~Q(requirement_type='checkbox') &
           Q(original_checkbox__isnull=True))
           |
          (Q(requirement_type='checkbox') &
           Q(original_checkbox__isnull=False))
        ),
        name='only_checkboxes_have_checkbox_field'
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
  target_checklist = models.ForeignKey(
    'UserChecklist',
    on_delete=models.CASCADE,
    related_name='depth_list'
  )
  courses = models.ManyToManyField(
    'progress.UserCourse', 
    related_name='depth_lists',
    blank=True
  )
  is_chain = models.BooleanField(blank=True, null=True)
  total_units = models.PositiveSmallIntegerField(default=0)
  num_courses = models.PositiveSmallIntegerField(default=0)

  class Meta:
    pass

@receiver(post_save, sender=UserDepthList)
def update_depth_list_counts_on_save(sender, instance, created, **kwargs):
  if instance.is_chain:
    num_courses = instance.courses.count()
  else:
    total_units = instance.courses.aggregate(
      total=Sum('units'))['total'] or 0
    num_courses = instance.courses.count()
  
  # Avoid recursion
  sender.objects.filter(pk=instance.pk).update(
    num_courses=num_courses,
    total_units=total_units if not instance.is_chain else instance.total_units
  )
