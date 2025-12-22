from rest_framework import serializers

from courses.models import Course, CourseRequisiteNode
from ..models.user_course import UserCourse, UserCoursePathNode
from courses.serializers import CourseListSerializer, CourseDetailSerializer
from .user_requirements_serializers import CourseMinimalSerializer


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
		

class UserPathNodeListSerializer(serializers.ModelSerializer):
	# Read-only method field that calls get_children on access
	target_course = CourseMinimalSerializer(read_only=True)
	requisite_node = serializers.PrimaryKeyRelatedField(
		queryset=CourseRequisiteNode.objects.all()
	)
	
	class Meta:
		model = UserCoursePathNode
		fields = [
			'id', 'created_at', 'updated_at', 'requisite_node', 'target_course'
		]
		

class UserPathNodeCreateSerializer(serializers.ModelSerializer):
	requisite_node = serializers.PrimaryKeyRelatedField(
		queryset=CourseRequisiteNode.objects.all()
	)
	target_course = serializers.PrimaryKeyRelatedField(
		queryset=Course.objects.all()
	)
	parent_node = serializers.PrimaryKeyRelatedField(
		queryset=UserCoursePathNode.objects.all(),
		required=False
	)
	
	class Meta:
		model = UserCoursePathNode
		fields = [
			'id', 'created_at', 'updated_at', 'requisite_node', 'target_course',
			'parent_node'
		]
		read_only_fields = ['id', 'created_at', 'updated_at']

	def create(self, validated_data):
		parent_node = validated_data.pop('parent_node', None)
		if parent_node:
			parent_node = validated_data['parent_node']
			new_node = parent_node.add_child(**validated_data)
		else:
			new_node = UserCoursePathNode.add_root(**validated_data)
		return new_node
	