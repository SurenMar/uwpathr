from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend

from ..models.user_course import UserCourse
from ..models.user_requirements import (
  UserAdditionalConstraint, 
  UserDepthList,
)
from ..serializers.user_requirements_serializers import (
  UserAdditionalConstraintsListSerializer,
  UserDepthListListSerializer,
)


class UserAdditionalConstraintViewSet(ReadOnlyModelViewSet):
  # Flexible filtering, searching, and ordering
  filter_backends = [DjangoFilterBackend]
  filterset_fields = {
    'target_checklist': ['exact'],
  }

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
    return UserAdditionalConstraintsListSerializer
  

class UserDepthListViewSet(ReadOnlyModelViewSet):
  # Flexible filtering, searching, and ordering
  filter_backends = [DjangoFilterBackend]
  filterset_fields = {
    'target_checklist': ['exact'],
  }

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
    return UserDepthListListSerializer
