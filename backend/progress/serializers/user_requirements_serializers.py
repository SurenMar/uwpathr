from rest_framework import serializers
from django.db import transaction

from progress.models.user_requirements import (
  UserAdditionalConstraint, 
  UserDepthList,
)
from progress.models.user_course import UserCourse
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
      'id', 'created_at', 'updated_at', 'requirement_type', 'title', 'selected_course',
      'num_courses_required', 'num_courses_gathered', 'completed',
    ]
    read_only_fields = [
      'id', 'created_at', 'updated_at', 'title', 'requirement_type',
      'num_courses_required', 'num_courses_gathered'
    ]

  def validate_selected_course(self, value):
    # Allow unsetting the course
    if value is None:
      return value
    
    # Only checkboxes can have selected courses
    if self.instance and self.instance.requirement_type != 'checkbox':
      raise serializers.ValidationError(
        "Only checkbox nodes can have selected courses."
      )
    
    # For updates, verify course is in allowed list
    if self.instance and self.instance.original_checkbox:
      # Get the AdditionalConstraintAllowedCourses object
      allowed_courses_obj = self.instance.original_checkbox.allowed_courses.first()
      # Validate the selection
      if not allowed_courses_obj.courses.filter(pk=value.pk).exists():
        raise serializers.ValidationError(
          "Selected course is not in allowed courses."
        )
    
    return value

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
        parent.num_courses_gathered = max(0, min(parent.num_courses_required, parent.num_courses_gathered))
        if parent.num_courses_gathered == parent.num_courses_required:
          parent.completed = True
        parent.save(update_fields=['num_courses_gathered', 'completed'])

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


class UserDepthListDetailSerializer(serializers.ModelSerializer):
  courses = UserCourseMinimalSerializer(many=True, read_only=True)

  class Meta:
    model = UserDepthList
    fields = [
      'id', 'created_at', 'updated_at', 'courses', 'is_chain', 'total_units',
      'num_courses'
    ]


class UserDepthListCreateSerializer(serializers.ModelSerializer):
  class Meta:
    model = UserDepthList
    fields = [
      'id', 'created_at', 'updated_at', 'courses', 'is_chain'
    ]
    read_only_fields = ['id', 'created_at', 'updated_at', 'courses']


class UserDepthListUpdateSerializer(serializers.ModelSerializer):
  courses = serializers.PrimaryKeyRelatedField(
    many=True, queryset=UserCourse.objects.all()
  )

  class Meta:
    model = UserDepthList
    fields = [
      'id', 'created_at', 'updated_at', 'courses', 'is_chain'
    ]
    read_only_fields = ['id', 'created_at', 'updated_at']
  
