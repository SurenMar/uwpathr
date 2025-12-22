from django.db import models, transaction
from django.db.models import Q
from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from mptt.models import MPTTModel, TreeForeignKey


class UserChecklist(models.Model):
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  year = models.PositiveSmallIntegerField()
  user = models.ForeignKey(
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
  original_checklist = models.ForeignKey(
    'checklists.Checklist',
    on_delete=models.CASCADE,
    related_name='+'
  )
  # TODO Add indexing and ordering for frontend csr
  class Meta:
    constraints = [
      models.UniqueConstraint(
        fields=['user', 'specialization'],
        name='unique_specialization_per_user'
      )
    ]


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
  completed = models.BooleanField(default=False)
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
  selected_course = models.OneToOneField( # A course can only be selected once
    'courses.Course',
    blank=True,
    null=True,
    on_delete=models.SET_NULL,
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
        ),
        name='only_groups_have_units'
      ),
      models.CheckConstraint(
        check=(
          (~Q(requirement_type='checkbox') &
           Q(original_checkbox__isnull=True) &
           Q(selected_course__isnull=True))
           |
          (Q(requirement_type='checkbox') &
           Q(original_checkbox__isnull=False) &
           Q(selected_course__isnull=False))
        ),
        name='only_checkboxes_have_course_and_checkbox_field'
      )
    ]

@receiver(post_save, sender=UserChecklistNode)
def update_parent_on_child_update(sender, instance, created, **kwargs):
  if not created and instance.requirement_type == 'checkbox' and \
     instance.parent.requirement_type == 'group':
    old = sender.objects.get(pk=instance.pk)
    update_group_on_course_change(old, instance)
    instance = instance.parent
  
  if not created and instance.requirement_type == 'group' and \
     instance.parent.requirement_type == 'head':
    update_head_on_group_change(instance)
    
def update_group_on_course_change(old_instance, new_instance):
  parent = getattr(new_instance, 'parent', None)
  if parent is None:
    return  # nothing to update

  old_units = old_instance.selected_course.units \
    if old_instance.selected_course else 0
  new_units = new_instance.selected_course.units \
    if new_instance.selected_course else 0

  # Update units_gathered safely
  with transaction.atomic():
    # Use update() to avoid triggering signals on parent
    type(parent).objects.filter(pk=parent.pk).update(
      units_gathered=parent.units_gathered - old_units + new_units
    )

def update_head_on_group_change(new_instance):
  parent = getattr(new_instance, 'parent', None)
  if parent is None:
    return  # nothing to update

  if new_instance.units_gathered == new_instance.units_required:
    # Update parent safely
    with transaction.atomic():
      parent.completed = True
      # Save only the completed field
      type(parent).objects.filter(pk=parent.pk).update(completed=True)
    
