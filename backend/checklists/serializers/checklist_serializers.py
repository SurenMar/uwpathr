from rest_framework import serializers
from django.db import transaction
from ..models.checklist import (
  Checklist,
  ChecklistNode,
  CheckboxAllowedCourses,
)

class ChecklistListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Checklist
    fields = [
      'id', 'created_at', 'updated_at', 'year', 'units_required', 
      'specialization',
    ]
    read_only_fields = ['id', 'created_at', 'updated_at']

class ChecklistCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = Checklist
    fields = [
      'year', 'units_required', 'specialization'
    ]


class ChecklistNodeListSerializer(serializers.ModelSerializer):
	# Read-only method field that calls get_children on access
	children = serializers.SerializerMethodField()
	
	class Meta:
		model = ChecklistNode
		fields = [
			'id', 'created_at', 'updated_at', 'requirement_type', 'title',
			'units_required', 'target_checklist', 'children',
		]
		read_only_fields = ['id', 'created_at', 'updated_at', 'target_checklist']

	def get_children(self, obj):
		# Assumes queryset is prefetched in view
		children = obj.get_children()
		return ChecklistNodeListSerializer(children, many=True).data
	

class ChecklistNodeCreateSerializer(serializers.ModelSerializer):
	# Write-only method field for POST
	children_input = serializers.ListField(
		child=serializers.DictField(),
		write_only=True,
		required=False
	)

	class Meta:
		model = ChecklistNode
		fields = [
			'requirement_type', 'title', 'units_required', 'target_checklist', 
			'children', 'children_input',
		]

	@transaction.atomic
	def create(self, validated_data):
		children_data = validated_data.pop('children_input', [])
		node = ChecklistNode.objects.create(**validated_data)
		
		# Recursively create children
		for child_data in children_data:
			ChecklistNodeCreateSerializer().create({
				**child_data,
				'parent': node,
				'target_checklist': node.target_checklist,
				'requirement_type': node.requirement_type,
			})
		return node


