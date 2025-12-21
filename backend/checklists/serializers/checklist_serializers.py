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
