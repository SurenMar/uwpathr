from rest_framework import serializers
from django.db import transaction
from .models import Course, CourseRequisiteNode


class CourseSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = [
			'id', 'created_at', 'updated_at',
			'code', 'number', 'units', 'offered_next_term', 'category',
			'title', 'description', 'num_uwflow_ratings', 'uwflow_liked_rating', 
			'uwflow_easy_ratings', 'uwflow_useful_ratings',
		]
		read_only_fields = ['id', 'created_at', 'updated_at']


class CourseRequisiteNodeSerializer(serializers.ModelSerializer):
	"""
	Nested serializer for MPPT tree structure.
	On retrieve: returns tree with nested children.
	On create: accepts nested structure and recursively creates tree atomically.
	"""
	# Read-only method field that calls get_children on access
	children = serializers.SerializerMethodField()
	# Write-only method field for POST
	children_input = serializers.ListField(
		child=serializers.DictField(),
		write_only=True,
		required=False
	)
	
	class Meta:
		model = CourseRequisiteNode
		fields = [
			'id', 'created_at', 'updated_at',
			'requisite_type', 'target_course', 'node_type',
			'leaf_course', 'num_children_required', 'children', 'children_input',
		]
		read_only_fields = ['id', 'created_at', 'updated_at', 'target_course']

	def get_children(self, obj):
		# Assumes queryset is prefetched in view
		children = obj.get_children()
		return CourseRequisiteNodeSerializer(children, many=True).data

	@transaction.atomic
	def create(self, validated_data):
		children_data = validated_data.pop('children_input', [])
		node = CourseRequisiteNode.objects.create(**validated_data)
		
    # Recursively create children
		for child_data in children_data:
			CourseRequisiteNodeSerializer().create({
				**child_data,
				'parent': node,
				'target_course': node.target_course,
				'requisite_type': node.requisite_type,
      })
		return node
