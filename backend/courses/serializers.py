from rest_framework import serializers
from django.db import transaction
from .models import Course, CourseRequisiteNode


class CourseListSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = [
			'code', 'number', 'units', 'category', 'title', 'num_uwflow_ratings', 
			'uwflow_liked_rating', 'uwflow_easy_ratings', 'uwflow_useful_ratings',
		]


class CourseDetailSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = [
			'id', 'created_at', 'updated_at', 'code', 'number', 'units', 
			'offered_next_term', 'category', 'title', 'description', 
			'num_uwflow_ratings', 'uwflow_liked_rating', 'uwflow_easy_ratings', 
			'uwflow_useful_ratings',
		]
		read_only_fields = ['id', 'created_at', 'updated_at']
		

class CourseCreateSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = [
			'code', 'number', 'units', 'category', 'title', 'num_uwflow_ratings', 
			'uwflow_liked_rating', 'uwflow_easy_ratings', 'uwflow_useful_ratings',
		]
		

class CourseRequisiteNodeListSerializer(serializers.ModelSerializer):
	# Read-only method field that calls get_children on access
	children = serializers.SerializerMethodField()
	
	class Meta:
		model = CourseRequisiteNode
		fields = [
			'id', 'created_at', 'updated_at',
			'requisite_type', 'target_course', 'node_type',
			'leaf_course', 'num_children_required', 'children',
		]
		read_only_fields = ['id', 'created_at', 'updated_at', 'target_course']

	def get_children(self, obj):
		# Assumes queryset is prefetched in view
		children = obj.get_children()
		return CourseRequisiteNodeListSerializer(children, many=True).data
	

class CourseRequisiteNodeCreateSerializer(serializers.ModelSerializer):
	# Write-only method field for POST
	children_input = serializers.ListField(
		child=serializers.DictField(),
		write_only=True,
		required=False
	)

	class Meta:
		model = CourseRequisiteNode
		fields = [
			'requisite_type', 'target_course', 'node_type', 'leaf_course', 
			'num_children_required', 'children', 'children_input',
		]

	@transaction.atomic
	def create(self, validated_data):
		children_data = validated_data.pop('children_input', [])
		node = CourseRequisiteNode.objects.create(**validated_data)
		
		# Recursively create children
		for child_data in children_data:
			CourseRequisiteNodeCreateSerializer().create({
				**child_data,
				'parent': node,
				'target_course': node.target_course,
				'requisite_type': node.requisite_type,
			})
		return node

