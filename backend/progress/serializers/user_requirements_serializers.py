from rest_framework import serializers
from django.db import transaction

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
  

class UserAdditionalConstraintsUpdateSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserAdditionalConstraint
    fields = [
      'id', 'created_at', 'updated_at', 'requirement_type', 'title', 
      'num_courses_required', 'num_courses_gathered', 'completed',
    ]
    read_only_fields = [
      'id', 'created_at', 'updated_at', 'title', 'requirement_type',
      'num_courses_required', 'num_courses_gathered'
    ]

  def update(self, instance, validated_data):
    completed = validated_data.get('completed', instance.completed)
    parent = instance.parent

    if instance.requirement_type == 'checkbox' and parent:
      with transaction.atomic():
        # Update parent counter
        if completed and not instance.completed:
          parent.num_courses_gathered += 1
        elif not completed and instance.completed:
          parent.num_courses_gathered -= 1
        # Clamp values
        parent.num_courses_gathered = max(0, min(parent.num_required_courses, parent.num_courses_gathered))
        parent.save(update_fields=['num_courses_gathered'])

        # Update child
        instance.completed = completed
        instance.save(update_fields=['completed'])
    return instance


class CourseMinimalSerializer(serializers.ModelSerializer):
  class Meta:
    model = Course
    fields = ['id', 'code', 'number']


class UserCourseMinimalSerializer(serializers.ModelSerializer):
  course = CourseMinimalSerializer(read_only=True)

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
