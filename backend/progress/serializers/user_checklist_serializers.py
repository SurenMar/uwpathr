from rest_framework import serializers
from django.db import transaction
from progress.models.user_checklist import UserChecklist, UserChecklistNode
from progress.models.user_requirements import UserAdditionalConstraint
from checklists.models.checklist import Checklist, ChecklistNode
from checklists.models.requirements import AdditionalConstraint


class UserChecklistNodeListSerializer(serializers.ModelSerializer):
  children = serializers.SerializerMethodField()

  class Meta:
    model = UserChecklistNode
    fields = [
      'id', 'created_at', 'updated_at', 'requirement_type', 'title', 
      'units_required', 'units_gathered', 'completed', 'selected_course',
      'children',
    ]

  def get_children(self, obj):
		# Assumes queryset is prefetched in view
    children = obj.get_children()
    if not children:
      return []
    return UserChecklistNodeListSerializer(
      children, 
      many=True,
      context=self.context
    ).data


class UserChecklistNodeUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserChecklistNode
    fields = [
      'id', 'created_at', 'updated_at', 'requirement_type', 'selected_course'
    ]
    read_only_fields = ['id', 'created_at', 'updated_at', 'requirement_type']

  def validate_selected_course(self, value):
    # Allow unsetting the course
    if value is None:
      return value
    
    # Only checkboxes can have selected courses
    if self.instance and self.instance.requirement_type != 'checkbox':
      raise serializers.ValidationError(
        "Only checkbox nodes can have selected courses."
      )
    
    # For updates, verify course is in allowed list
    if self.instance and self.instance.original_checkbox:
      if self.instance.original_checkbox.allowed_courses.courses.exists():
        return value
      allowed_courses = self.instance.original_checkbox.allowed_courses.courses.all()
      if not allowed_courses.filter(pk=value.pk).exists():
        raise serializers.ValidationError(
          "Selected course is not in allowed courses."
        )
    
    return value
    

  def update(self, instance, validated_data):
    if 'selected_course' in validated_data and \
       instance.requirement_type == 'checkbox':
      instance.selected_course = validated_data['selected_course']
    instance.save(update_fields=['selected_course'])
    return instance


class UserChecklistDetailSerializer(serializers.ModelSerializer):
  nodes = serializers.SerializerMethodField()

  class Meta:
    model = UserChecklist
    fields = [
      'id', 'created_at', 'updated_at', 'year', 'units_required',
      'taken_course_units', 'planned_course_units', 'specialization',
      'nodes',
    ]

  def get_nodes(self, obj):
    # Filter roots from the prefetched node set
    roots = [n for n in obj.nodes.all() if n.parent_id is None]
    return UserChecklistNodeListSerializer(
      roots, 
      many=True,
      context=self.context
    ).data


class UserChecklistCreateSerializer(serializers.Serializer):
  year = serializers.IntegerField()
  specialization = serializers.IntegerField()

  def validate(self, data):
    # Check if checklist exists
    try:
      checklist = Checklist.objects.get(
        year=data['year'],
        specialization_id=data['specialization']
      )
      data['original_checklist'] = checklist
    except Checklist.DoesNotExist:
      raise serializers.ValidationError(
        "Checklist not found for given year and specialization"
      )
    
    # Check if user already has this checklist
    user = self.context['request'].user
    if UserChecklist.objects.filter(
      user=user,
      specialization_id=data['specialization']
    ).exists():
      raise serializers.ValidationError(
        "User already has a checklist for this specialization"
      )
    
    return data

  def create(self, validated_data):
    user = self.context['request'].user
    original_checklist = validated_data['original_checklist']
    
    with transaction.atomic():
      # Create UserChecklist
      user_checklist = UserChecklist.objects.create(
        year=validated_data['year'],
        user=user,
        units_required=original_checklist.units_required,
        specialization_id=validated_data['specialization'],
        original_checklist=original_checklist,
        taken_course_units=0,
        planned_course_units=0
      )

      # Copy ChecklistNode tree
      self._copy_checklist_nodes(original_checklist, user_checklist, user)
      
      # Copy AdditionalConstraint tree
      self._copy_additional_constraints(original_checklist, user_checklist, user)

    return user_checklist
  
  def to_representation(self, instance):
    """Return detailed representation using UserChecklistDetailSerializer"""
    serializer = UserChecklistDetailSerializer(instance, context=self.context)
    return serializer.data

  def _copy_checklist_nodes(self, original_checklist, user_checklist, user):
    """Copy ChecklistNode tree to UserChecklistNode"""
    node_map = {}  # Maps original node id to new user node
    checklist_nodes = ChecklistNode.objects.filter(
      target_checklist=original_checklist
    ).order_by('tree_id', 'lft')  # MPTT ordering

    # Create nodes sequentially so MPTT fields (lft/rgt) are populated
    for original_node in checklist_nodes:
      parent = node_map.get(original_node.parent_id) if original_node.parent_id else None
      user_node = UserChecklistNode.objects.create(
        requirement_type=original_node.requirement_type,
        title=original_node.title,
        units_required=original_node.units_required,
        units_gathered=0 if original_node.requirement_type == 'group' else None,
        completed=False,
        user=user,
        target_checklist=user_checklist,
        original_checkbox=original_node if original_node.requirement_type == 'checkbox' else None,
        selected_course=None,
        parent=parent
      )
      node_map[original_node.id] = user_node

  def _copy_additional_constraints(self, original_checklist, user_checklist, user):
    """Copy AdditionalConstraint tree to UserAdditionalConstraint"""
    constraint_map = {}  # Maps original constraint id to new user constraint
    additional_constraints = AdditionalConstraint.objects.filter(
      target_checklist=original_checklist
    ).order_by('tree_id', 'lft')  # MPTT ordering

    # Create constraints sequentially so MPTT fields (lft/rgt) are populated
    for original_constraint in additional_constraints:
      parent = constraint_map.get(original_constraint.parent_id) if original_constraint.parent_id else None
      user_constraint = UserAdditionalConstraint.objects.create(
        title=original_constraint.title,
        requirement_type=original_constraint.requirement_type,
        num_courses_required=original_constraint.num_courses_required,
        num_courses_gathered=0 if original_constraint.requirement_type == 'group' else None,
        completed=False,
        user=user,
        target_checklist=user_checklist,
        original_checkbox=original_constraint if original_constraint.requirement_type == 'checkbox' else None,
        parent=parent
      )
      constraint_map[original_constraint.id] = user_constraint

