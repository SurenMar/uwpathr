from rest_framework import serializers

from courses.models import Course, CoursePrerequisiteNode
from progress.models.user_course import UserCourse, UserCoursePathNode
from courses.serializers import CourseListSerializer, CourseDetailSerializer
from progress.serializers.user_requirements_serializers import UserCourseMinimalSerializer


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
	target_course = UserCourseMinimalSerializer(read_only=True)
	prerequisite_node = serializers.PrimaryKeyRelatedField(
		queryset=CoursePrerequisiteNode.objects.all()
	)
	
	class Meta:
		model = UserCoursePathNode
		fields = [
			'id', 'created_at', 'updated_at', 'prerequisite_node', 'target_course',
			'branch_completed'
		]
		

class UserPathNodeCreateSerializer(serializers.Serializer):
	prerequisite_node = serializers.PrimaryKeyRelatedField(
		queryset=CoursePrerequisiteNode.objects.all()
	)
	target_course = serializers.PrimaryKeyRelatedField(
		queryset=UserCourse.objects.filter(
			course_list__in=['planned', 'wishlist'])
	)
	children = serializers.ListField(
		child=serializers.DictField(),
		required=False,
		default=[]
	)

	def validate(self, data):
		def validate_node(node):
			# Required keys
			required_keys = {'target_course', 'prerequisite_node'}
			missing = required_keys - node.keys()
			if missing:
				raise serializers.ValidationError(
					f"Missing required fields: {missing}"
				)

			# Validate that IDs exist (handle both objects and IDs)
			prereq = node['prerequisite_node']
			prereq_id = prereq.id if hasattr(prereq, 'id') else prereq
			if not CoursePrerequisiteNode.objects.filter(pk=prereq_id).exists():
				raise serializers.ValidationError(
					f"CoursePrerequisiteNode {prereq_id} does not exist"
				)
			
			target = node['target_course']
			target_id = target.id if hasattr(target, 'id') else target
			if not UserCourse.objects.filter(pk=target_id).exists():
				raise serializers.ValidationError(
					f"UserCourse {target_id} does not exist"
				)

			# Type checks and recursive validation
			children = node.get('children', [])
			if not isinstance(children, list):
				raise serializers.ValidationError(
					"children must be a list"
				)

			for child in children:
				if not isinstance(child, dict):
					raise serializers.ValidationError(
						"Each child must be an object"
					)
				validate_node(child)

		validate_node(data)
		return data

	