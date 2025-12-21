from rest_framework.viewsets import ModelViewSet
from django.db.models import Prefetch
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, filters

from ..models.checklist import (
  Checklist, 
  ChecklistNode,
  CheckboxAllowedCourses,
)
from ..serializers.checklist_serializers import (
  ChecklistListSerializer,
  ChecklistCreateSerializer,
)


class Admin(BasePermission):
    def has_permission(self, request, view):
      return request.user and request.user.is_staff


class CourseFilter(FilterSet):
  # Comma-separated categories; matches any overlap in ArrayField
  category = filters.CharFilter(method='filter_category')
  offered_next_term = filters.BooleanFilter(field_name='offered_next_term')
  min_number = filters.NumberFilter(field_name='number', lookup_expr='gte')
  max_number = filters.NumberFilter(field_name='number', lookup_expr='lt')

  class Meta:
    model = Course
    fields = ['code', 'number', 'offered_next_term']

  def filter_category(self, queryset, name, value):
    values = [v.strip() for v in value.split(',') if v.strip()]
    if not values:
      return queryset
    # ArrayField overlap: returns rows where category overlaps with provided list
    return queryset.filter(category__overlap=values)


class ChecklistViewSet(ModelViewSet):
  queryset = Checklist.objects.select_related (
    # Foreign keys
    'specialization',
  ).all()
  permission_classes = [Admin]

  def get_serializer_class(self):
    if self.action in ('list', 'retrieve'):
      return ChecklistListSerializer
    elif self.action in ('create', 'update', 'partial_update'):
      return ChecklistCreateSerializer
    return ChecklistListSerializer
  

class ChecklistNodeViewSet(ModelViewSet):
   
  