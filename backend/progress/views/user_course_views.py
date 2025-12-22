from rest_framework.viewsets import ModelViewSet
from django.db.models import Prefetch
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, filters

from ..models.user_course import UserCourse, UserCoursePathNode
from ..serializers.user_course_serializers import (
  UserCourseListSerializer,
  UserCourseDetailSerializer,
  UserCourseCreateSerializer,

  UserPathNodeListSerializer,
  UserPathNodeCreateSerializer
) 


class UserCourseFilter(FilterSet):
  course_list = filters.CharFilter(method='filter_course_list')
  category = filters.CharFilter(method='filter_category')
  offered_next_term = filters.BooleanFilter(field_name='course__offered_next_term')
  min_number = filters.NumberFilter(field_name='course__number', lookup_expr='gte')
  max_number = filters.NumberFilter(field_name='course__number', lookup_expr='lt')

  class Meta:
    model = UserCourse
    fields = [
      'id', 'course__code', 'course__number', 'course__offered_next_term'
    ]
  
  def filter_course_list(self, queryset, name, value):
    values = [v.strip() for v in value.split(',') if v.strip()]
    if not values:
      return queryset
    # ArrayField overlap: returns rows where course_list overlaps with provided list
    return queryset.filter(course_list__overlap=values)
  
  def filter_category(self, queryset, name, value):
    values = [v.strip() for v in value.split(',') if v.strip()]
    if not values:
      return queryset
    # ArrayField overlap: returns rows where category overlaps with provided list
    return queryset.filter(category__overlap=values)


class UserCourseViewSet(ModelViewSet):
  http_method_names = ['get', 'post', 'delete']

  # Flexible filtering, searching, and ordering
  filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
  filterset_class = UserCourseFilter
  search_fields = ['course__code', 'course__number']
  ordering_fields = [
    'course__code', 'course__number', 'course__num_uwflow_ratings',
    'course__uwflow_liked_rating', 'course__uwflow_easy_ratings', 
    'course__uwflow_useful_ratings'
  ]
  ordering = ['course__code', 'course__number']

  def get_queryset(self):
    return (
      UserCourse.objects
      .filter(user=self.request.user)
      .select_related(
        'course'
      ).order_by('course__code', 'course__number')
    )

  def get_serializer_class(self):
    if self.action == 'list':
      return UserCourseListSerializer
    elif self.action == 'retrieve':
      return UserCourseDetailSerializer
    elif self.action in ['create', 'update', 'partial_update']:
      return UserCourseCreateSerializer
    return UserCourseDetailSerializer
  

class UserPathNodeViewSet(ModelViewSet):
  http_method_names = ['get', 'patch', 'delete']

  filter_backends = [DjangoFilterBackend]
  filterset_fields = {
    'target_course': ['exact'],
    'requisite_node': ['exact'],
  }

  def get_queryset(self):
    return (
      UserCourse.objects
      .filter(user=self.request.user)
      .select_related(
        'target_course',
        'requisite_node',
      ).order_by(
        'requisite_node__tree_id',
        'requisite_node__lft'
      )
    )

  def get_serializer_class(self):
    if self.action in ('list', 'retrieve'):
      return UserPathNodeListSerializer
    elif self.action == 'create':
      return UserPathNodeCreateSerializer
    return UserPathNodeListSerializer
