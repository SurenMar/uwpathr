from rest_framework import serializers

from courses.models import Course, CoursePrerequisiteNode
from progress.models.user_course import UserCourse, UserCoursePathNode
from courses.serializers import CourseListSerializer, CourseDetailSerializer
from progress.serializers.user_requirements_serializers import CourseMinimalSerializer


class UserCourseListSerializer(serializers.ModelSerializer):
	course = CourseListSerializer(read_only=True)

	class Meta:
		model = UserCourse
		fields = [
			'id', 'created_at', 'updated_at', 'course', 'course_list',
		]


class UserCourseDetailSerializer(serializers.ModelSerializer):
	course = CourseDetailSerializer(read_only=True)

	class Meta:
		model = UserCourse
		fields = [
			'id', 'created_at', 'updated_at', 'course', 'course_list'
		]
		

class UserCourseCreateSerializer(serializers.ModelSerializer):
	course = serializers.PrimaryKeyRelatedField(
		queryset=Course.objects.all()
	)

	class Meta:
		model = UserCourse
		fields = [
			'id', 'created_at', 'updated_at', 'course', 'course_list'
		]
		read_only_fields = ['id', 'created_at', 'updated_at']

	def validate(self, attrs):
		# Check if user has correct prerequisites to add course:
		if attrs.get('course_list') == 'taken' :
			course = attrs.get('course')
			try:
				root = CoursePrerequisiteNode.objects.get(
					target_course=course,
					parent=None,
				)
			# Succeed if course has no required prereqs
			except CoursePrerequisiteNode.DoesNotExist:
				return attrs

			prereq_subtree = root.get_descendants(include_self=True)
			taken_courses = set(
				UserCourse.objects
				.filter(
					user = self.context['request'].user, 
					course_list='taken'
				).values_list('course_id', flat=True)
			)

			# Build prereq tree:
			children_map = {}
			for node in prereq_subtree:
				children_map.setdefault(node.parent_id, []).append(node)

			def prereqs_taken(node):
				"""Recursive function that checks if all prereqs have been taken"""
				# Base case:
				if node.node_type == 'course':
					return node.leaf_course_id in taken_courses
				# Recursive case:
				else:
					prereq_match_count = 0
					for child in children_map.get(node.id, []):
						if prereqs_taken(child):
							prereq_match_count += 1
					return prereq_match_count >= node.num_children_required

			if prereqs_taken(root):
				return attrs
			else:
				raise serializers.ValidationError(
					"Prerequisites for this course have not been met"
				)

		return attrs
		

class UserPathNodeListSerializer(serializers.ModelSerializer):
	# Read-only method field that calls get_children on access
	target_course = CourseMinimalSerializer(read_only=True)
	prerequisite_node = serializers.PrimaryKeyRelatedField(
		queryset=CoursePrerequisiteNode.objects.all()
	)
	
	class Meta:
		model = UserCoursePathNode
		fields = [
			'id', 'created_at', 'updated_at', 'prerequisite_node', 'target_course'
		]
		

class UserPathNodeCreateSerializer(serializers.ModelSerializer):
	prerequisite_node = serializers.PrimaryKeyRelatedField(
		queryset=CoursePrerequisiteNode.objects.all()
	)
	target_course = serializers.PrimaryKeyRelatedField(
		queryset=UserCourse.objects.filter(course_list__in=[
			'planned',
			'wishlist',
		])
	)
	parent_node = serializers.PrimaryKeyRelatedField(
		queryset=UserCoursePathNode.objects.all(),
		required=False,
		allow_null=True,
		write_only=True,
	)
	
	class Meta:
		model = UserCoursePathNode
		fields = [
			'id', 'created_at', 'updated_at', 'prerequisite_node', 'target_course',
			'parent_node'
		]
		read_only_fields = ['id', 'created_at', 'updated_at']

	def create(self, validated_data):
		parent_node = validated_data.pop('parent_node', None)
		if parent_node:
			new_node = parent_node.add_child(**validated_data)
		else:
			new_node = UserCoursePathNode.add_root(**validated_data)
		return new_node
	