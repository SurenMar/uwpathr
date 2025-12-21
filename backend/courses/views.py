from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import BasePermission, SAFE_METHODS
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, filters

from .models import Course, CourseRequisiteNode
from .serializers import CourseSerializer, CourseRequisiteNodeSerializer


class ReadOnlyOrAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
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


class CourseViewSet(ModelViewSet):
  queryset = Course.objects.all().order_by('code', 'number')
  serializer_class = CourseSerializer
  permission_classes = [ReadOnlyOrAdmin]

  # Flexible filtering, searching, and ordering
  filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
  filterset_class = CourseFilter
  search_fields = ['code', 'number']
  ordering_fields = [
    'code', 'number', 'num_uwflow_ratings', 'uwflow_liked_rating', 
    'uwflow_easy_ratings', 'uwflow_useful_ratings'
  ]
  ordering = ['code', 'number']


class CourseRequisiteNodeViewSet(ModelViewSet):
  """
  ViewSet for MPTT model
  """
  queryset = CourseRequisiteNode.objects.all()
  serializer_class = CourseRequisiteNodeSerializer
  permission_classes = [ReadOnlyOrAdmin]

  filter_backends = [DjangoFilterBackend]
  filterset_fields = {
    'target_course': ['exact'], 
    'target_course__code': ['exact'], 
    'target_course__number': ['exact'], 
    'requisite_type': ['exact'],
  }
