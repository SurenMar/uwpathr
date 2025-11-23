from django.db import models
from django.db.models import Q
from mptt.models import MPTTModel, TreeForeignKey
from django.dispatch import receiver
from django.db.models.signals import (
  m2m_changed, 
  post_save,
  pre_delete
)


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
  user = models.OneToOneField(
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
          (Q(num_requirement_type='group') &
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
           Q(original_checkbox__isnull=True))
        ),
        name='only_checkboxes_have_checkbox_field'
      )
    ]

# Auto-save logic
@receiver(post_save, sender=UserAdditionalConstraint)
def update_parent_on_checkbox_add(sender, instance, created, **kwargs):
    if created and instance.requirement_type == 'checkbox' and \
       instance.parent and instance.parent.requirement_type == 'group':
      instance.parent.num_courses_gathered += 1
      instance.parent.save(update_fields=['num_courses_gathered'])

# Auto-delete logic
@receiver(pre_delete, sender=UserAdditionalConstraint)
def update_parent_on_checkbox_delete(sender, instance, created, **kwargs):
  if instance.requirement_type == 'checkbox' and \
     instance.parent and instance.parent.requirement_type == 'group':
    instance.parent.num_courses_gathered -= 1
    instance.parent.save(update_fields=['num_courses_gathered'])


# Maybe we have an auto fill button that creates a depth list on command
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
  total_units = models.PositiveSmallIntegerField()
  num_courses = models.PositiveSmallIntegerField()

  class Meta:
   # TODO Rework indexes and ordering for frontend csr
   pass

# Auto-add logic
@receiver(m2m_changed, sender=UserDepthList.courses.through)
def update_depth_list_on_add(sender, instance, action, pk_set, **kwargs):
  if action == 'post_add':
    added_courses = instance.courses.filter(pk__in=pk_set)
    for course in added_courses:
      if instance.is_chain:
        instance.num_courses += 1
      else:
        instance.total_units += course.course.units
    instance.save(update_fields=["num_courses", "total_units"])

# Auto-remove logic
@receiver(m2m_changed, sender=UserDepthList.courses.through)
def update_depth_list_on_remove(sender, instance, action, pk_set, **kwargs):
  if action == 'pre_remove':
    removed_courses = instance.courses.filter(pk__in=pk_set)
    for course in removed_courses:
      if instance.is_chain:
        instance.num_courses -= 1
      else:
        instance.total_units -= course.course.units
    instance.save(update_fields=["num_courses", "total_units"])
