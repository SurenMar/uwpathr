from rest_framework.viewsets import ReadOnlyModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .models.checklist import CheckboxAllowedCourses
from .models.requirements import AdditionalConstraintAllowedCourses
from serializers import (
  CheckboxAllowedCoursesListSerializer,
  AdditionalConstraintAllowedCoursesListSerializer
)


class CheckboxAllowedCoursesViewSet(ReadOnlyModelViewSet):
  # Prefetch queryset
  queryset = CheckboxAllowedCourses.objects.select_related(
    # Foreign keys
    'target_checkbox',
  ).prefetch_related(
    # M2M fields
    'courses'
  )

  filter_backends = [DjangoFilterBackend]
  filterset_fields = {
    'target_course': ['exact'],
  }

  def get_serializer_class(self):
    return CheckboxAllowedCoursesListSerializer


class AdditionalConstraintAllowedCoursesViewSet(ReadOnlyModelViewSet):
  # Prefetch queryset
  queryset = AdditionalConstraintAllowedCourses.objects.select_related(
    # Foreign keys
    'target_checkbox',
  ).prefetch_related(
    # M2M fields
    'courses',
  )

  filter_backends = [DjangoFilterBackend]
  filterset_fields = {
    'target_course': ['exact'],
  }

  def get_serializer_class(self):
    return AdditionalConstraintAllowedCoursesListSerializer
  