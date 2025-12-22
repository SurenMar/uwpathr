from rest_framework import serializers
from .models.checklist import CheckboxAllowedCourses
from courses.models import Course


class CoursesMinimalSerializer(serializers.ModelSerializer):
	class Meta:
		model = Course
		fields = [
			'id', 'created_at', 'updated_at', 'code', 'number'
		]
		read_only_fields = ['id', 'created_at', 'updated_at']


class CheckboxAllowedCoursesListSerializer(serializers.ModelSerializer):
	courses = CoursesMinimalSerializer(many=True, read_only=True)

	class Meta:
		model = CheckboxAllowedCourses
		fields = [
		  'id', 'created_at', 'updated_at', 'target_checkbox', 'courses',
    ]
		read_only_fields = ['id', 'created_at', 'updated_at', 'courses']


class AdditionalConstraintAllowedCoursesListSerializer(serializers.ModelSerializer):
	courses = CoursesMinimalSerializer(many=True, read_only=True)

	class Meta:
		model = CheckboxAllowedCourses
		fields = [
		  'id', 'created_at', 'updated_at', 'target_checkbox', 'courses',
    ]
		read_only_fields = ['id', 'created_at', 'updated_at', 'courses']
		
