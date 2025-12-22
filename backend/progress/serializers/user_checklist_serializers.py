from rest_framework import serializers
from ..models.user_checklist import UserChecklist, UserChecklistNode


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

