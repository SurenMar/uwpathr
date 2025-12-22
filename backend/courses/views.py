from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import Prefetch
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, filters

from .models import Course, CourseRequisiteNode
from .serializers import (
  CourseListSerializer,
  CourseDetailSerializer,

  CourseRequisiteNodeListSerializer,
) 


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


class CourseViewSet(ReadOnlyModelViewSet):
  queryset = Course.objects.all().order_by('code', 'number')

  # Flexible filtering, searching, and ordering
  filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
  filterset_class = CourseFilter
  search_fields = ['code', 'number']
  ordering_fields = [
    'code', 'number', 'num_uwflow_ratings', 'uwflow_liked_rating', 
    'uwflow_easy_ratings', 'uwflow_useful_ratings'
  ]
  ordering = ['code', 'number']

  def get_serializer_class(self):
    if self.action == 'list':
      return CourseListSerializer
    elif self.action == 'retrieve':
      return CourseDetailSerializer


class CourseRequisiteNodeViewSet(ReadOnlyModelViewSet):
  """
  ViewSet for MPTT model
  """
  # Prefetch queryset
  queryset = CourseRequisiteNode.objects.select_related(
    # Foreign keys
    'target_course',
    'leaf_course',
  ).prefetch_related(
    Prefetch(
      # Reverse foreign keys
      'children', 
      queryset=CourseRequisiteNode.objects.all()
    )
  )

  filter_backends = [DjangoFilterBackend]
  filterset_fields = {
    'target_course': ['exact']
  }

  def get_serializer_class(self):
    return CourseRequisiteNodeListSerializer
