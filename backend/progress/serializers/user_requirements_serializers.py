from rest_framework import serializers

from ..models.user_requirements import (
  UserAdditionalConstraint, 
  UserDepthList,
)
from ..models.user_course import UserCourse
from courses.models import Course


class UserAdditionalConstraintsListSerializer(serializers.ModelSerializer):
  children = serializers.SerializerMethodField()

  class Meta:
    model = UserAdditionalConstraint
    fields = [
      'id', 'created_at', 'updated_at', 'requirement_type', 'title', 
      'num_courses_required', 'num_courses_gathered', 'completed', 'children',
    ]

  def get_children(self, obj):
		# Assumes queryset is prefetched in view
    children = obj.get_children()
    if not children:
      return []
    return UserAdditionalConstraintsListSerializer(
      children, 
      many=True,
      context=self.context
    ).data


class CourseMinimalSerializer(serializers.ModelSerializer):
  class Meta:
    model = Course
    fields = ['id', 'code', 'number']


class UserCourseMinimalSerializer(serializers.ModelSerializer):
  course = CourseMinimalSerializer(many=False, read_only=True)

  class Meta:
    model = UserCourse
    fields = ['id', 'course_list', 'course']


class UserDepthListListSerializer(serializers.ModelSerializer):
  courses = UserCourseMinimalSerializer(many=True, read_only=True)

  class Meta:
    model = UserDepthList
    fields = [
      'id', 'created_at', 'updated_at', 'courses', 'is_chain', 'total_units',
      'num_courses'
    ]
