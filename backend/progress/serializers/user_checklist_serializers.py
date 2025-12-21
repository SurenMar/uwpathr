from rest_framework import serializers
from ..models.user_checklist import UserChecklist, UserChecklistNode


class UserChecklistNodeSerializer(serializers.ModelSerializer):
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
    return UserChecklistNodeSerializer(children, many=True).data


class UserChecklistDetailSerializer(serializers.ModelSerializer):
  nodes = UserChecklistNodeSerializer(many=True, read_only=True)

  class Meta:
    model = UserChecklist
    fields = [
      'id', 'created_at', 'updated_at', 'year', 'units_required',
      'taken_course_units', 'planned_course_units', 'specialization',
      'nodes',
    ]
