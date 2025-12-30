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
  title = models.CharField(max_length=128)
  units_required = models.PositiveSmallIntegerField(blank=True, null=True)
  units_gathered = models.PositiveSmallIntegerField(blank=True, null=True)
  completed = models.BooleanField(default=False)
  user = models.ForeignKey(
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
           Q(original_checkbox__isnull=False))
        ),
        name='only_checkboxes_have_checkbox_field_checklist'
      )
    ]
  
  def save(self, *args, **kwargs):
    if self.pk:  # If updating existing instance
      try:
        old = UserChecklistNode.objects.get(pk=self.pk)
        self._old_selected_course = old.selected_course
      except UserChecklistNode.DoesNotExist:
        pass
    super().save(*args, **kwargs)

@receiver(post_save, sender=UserChecklistNode)
def update_parent_on_child_update(sender, instance, created, **kwargs):
  if created:
    return
  
  # Handle checkbox updates - update all parent groups
  if instance.requirement_type == 'checkbox' and instance.parent:
    # Get the old selected course from the instance attribute set in save()
    old_selected_course = getattr(instance, '_old_selected_course', None)
    update_all_parent_groups(old_selected_course, instance)
    
    # After updating groups, find and update the head
    head_parent = instance.parent
    while head_parent and head_parent.requirement_type == 'group':
      head_parent = head_parent.parent
    
    if head_parent and head_parent.requirement_type == 'head':
      update_head_on_group_change(head_parent)
  
  # Handle group updates - update parent head
  elif instance.requirement_type == 'group' and \
       instance.parent and instance.parent.requirement_type == 'head':
    update_head_on_group_change(instance)
    
def update_all_parent_groups(old_selected_course, checkbox_instance):
  """Update units_gathered for all parent groups (not just immediate parent)"""
  old_units = old_selected_course.units if old_selected_course else 0
  new_units = checkbox_instance.selected_course.units \
    if checkbox_instance.selected_course else 0
  units_delta = new_units - old_units
  
  # Traverse up through all group parents and update their units
  with transaction.atomic():
    parent = checkbox_instance.parent
    while parent and parent.requirement_type == 'group':
      # Update this group's units_gathered
      new_units_gathered = parent.units_gathered + units_delta
      
      # Check if group should be completed
      is_completed = new_units_gathered >= parent.units_required
      
      type(parent).objects.filter(pk=parent.pk).update(
        units_gathered=new_units_gathered,
        completed=is_completed
      )
      
      # Move to next parent
      parent = parent.parent

def update_head_on_group_change(group_instance):
  parent = group_instance.parent
  if parent is None:
    return

  # Propagate completion status up the tree with different logic based on type
  with transaction.atomic():
    while parent:
      # Different completion logic based on parent type
      if parent.requirement_type == 'head':
        # Head: all children must be completed
        is_completed = not parent.get_children().filter(completed=False).exists()
      elif parent.requirement_type == 'group':
        # Group: At least one group child completed AND units_gathered >= units_required
        # If no group children, only check units requirement
        group_children = parent.get_children().filter(requirement_type='group')
        
        if group_children.exists():
          # Has group children: at least one must be completed AND units requirement met
          has_completed_group_child = group_children.filter(completed=True).exists()
          units_requirement_met = parent.units_gathered >= parent.units_required
          is_completed = has_completed_group_child and units_requirement_met
        else:
          # No group children: only check units requirement
          is_completed = parent.units_gathered >= parent.units_required
      else:
        # Other types: skip
        parent = parent.parent
        continue
      
      if is_completed != parent.completed:
        type(parent).objects.filter(pk=parent.pk).update(completed=is_completed)
        # Refresh the parent to get the updated completed status
        parent.refresh_from_db()

      parent = parent.parent
    
