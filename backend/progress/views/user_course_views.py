from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, filters

from courses.models import CoursePrerequisiteNode
from progress.models.user_course import UserCourse, UserCoursePathNode
from progress.serializers.user_course_serializers import (
  UserCourseListSerializer,
  UserCourseDetailSerializer,
  UserCourseCreateSerializer,

  UserPathNodeListSerializer,
  UserPathNodeCreateSerializer,
) 


class UserCourseFilter(FilterSet):
  course_list = filters.CharFilter(method='filter_course_list')
  category = filters.CharFilter(method='filter_category')
  min_number = filters.NumberFilter(field_name='course__number', lookup_expr='gte')
  max_number = filters.NumberFilter(field_name='course__number', lookup_expr='lt')

  class Meta:
    model = UserCourse
    fields = [
      'id', 'course__code', 'course__number'
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
  
  def perform_create(self, serializer):
    # Delete entry if one already exists (course must be in at most 1 list)
    course = serializer.validated_data['course']
    user = self.request.user
    UserCourse.objects.filter(user=user, course=course).delete()

    serializer.save(user=self.request.user)
  

class UserPathNodeViewSet(ModelViewSet):
  @staticmethod
  def _create_tree_recursive(user, target_course_id, prerequisite_node_id, children, parent=None):
    # Fetch the objects from IDs
    prerequisite_node = CoursePrerequisiteNode.objects.get(pk=prerequisite_node_id)
    target_course = UserCourse.objects.get(pk=target_course_id)
    
    node = UserCoursePathNode.objects.create(
      user=user,
      target_course=target_course,
      prerequisite_node=prerequisite_node,
      branch_completed=False if prerequisite_node.node_type == 'group' else True,
      parent=parent
    )

    for child in children:
      UserPathNodeViewSet._create_tree_recursive(
        user,
        target_course_id,  # Same target course for all nodes in tree
        child['prerequisite_node'],
        child['children'],
        parent=node
      )

  http_method_names = ['get', 'post', 'delete']

  filter_backends = [DjangoFilterBackend]
  filterset_fields = {
    'target_course': ['exact'],
    'prerequisite_node': ['exact'],
  }

  def get_queryset(self):
    return (
      UserCoursePathNode.objects
      .filter(user=self.request.user)
      .select_related(
        'target_course',
        'prerequisite_node',
      ).order_by(
        'prerequisite_node__tree_id',
        'prerequisite_node__lft'
      )
    )

  def get_serializer_class(self):
    if self.action in ('list', 'retrieve'):
      return UserPathNodeListSerializer
    elif self.action == 'create':
      return UserPathNodeCreateSerializer
    return UserPathNodeListSerializer
  
  def perform_create(self, serializer):
    # Extract IDs (PrimaryKeyRelatedField converts to objects at top level)
    target_course_id = serializer.validated_data['target_course'].id
    prerequisite_node_id = serializer.validated_data['prerequisite_node'].id
    
    # Delete existing tree if it already exists for this target course
    UserCoursePathNode.objects.filter(
      user=self.request.user, 
      target_course_id=target_course_id,
    ).delete()
    
    UserPathNodeViewSet._create_tree_recursive(
      self.request.user,
      target_course_id,
      prerequisite_node_id,
      serializer.validated_data['children']
    )
