from rest_framework.viewsets import ModelViewSet
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend

from ..models.user_course import UserCourse
from ..models.user_requirements import (
  UserAdditionalConstraint, 
  UserDepthList,
)
from ..serializers.user_requirements_serializers import (
  UserAdditionalConstraintsListSerializer,
  UserAdditionalConstraintsUpdateSerializer,

  UserDepthListDetailSerializer,
  UserDepthListCreateSerializer,
  UserDepthListUpdateSerializer,
)


class UserAdditionalConstraintViewSet(ModelViewSet):
  # Flexible filtering, searching, and ordering
  filter_backends = [DjangoFilterBackend]
  filterset_fields = {
    'target_checklist': ['exact'],
  }
  http_method_names = ['get', 'patch']

  def get_queryset(self):
    return (
      UserAdditionalConstraint.objects
      .filter(user=self.request.user)
      .select_related(
        # Foreign keys
        'target_checklist',
        'original_checkbox',
      ).prefetch_related(
        # Reverse foreign keys
        'children',
      )
    )
  
  def get_serializer_class(self):
    if self.action in ('list', 'retrieve'):
      return UserAdditionalConstraintsListSerializer
    elif self.action == 'partial_update':
      return UserAdditionalConstraintsUpdateSerializer
    return UserAdditionalConstraintsListSerializer
  

class UserDepthListViewSet(ModelViewSet):
  filter_backends = [DjangoFilterBackend]
  filterset_fields = {
    'target_checklist': ['exact'],
  }
  http_method_names = ['get', 'create', 'patch']

  def get_queryset(self):
    return (
      UserDepthList.objects
      .filter(user=self.request.user)
      .select_related(
        # Foreign keys
        'target_checklist',
      ).prefetch_related(
        Prefetch(
          'courses',
          queryset=UserCourse.objects.select_related('course'),
        )
      )
    )
  
  def get_serializer_class(self):
    if self.action == 'retrieve':
      return UserDepthListDetailSerializer
    elif self.action == 'create':
      return UserDepthListCreateSerializer
    elif self.action == 'partial_update':
      return UserDepthListUpdateSerializer
    return UserDepthListDetailSerializer
