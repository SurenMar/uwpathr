from rest_framework.viewsets import ModelViewSet
from django.db.models import Prefetch
from rest_framework.permissions import BasePermission

from courses.models import Course
from ..models.checklist import (
  Checklist, 
  ChecklistNode,
  CheckboxAllowedCourses,
)
from ..serializers.checklist_serializers import (
  ChecklistListSerializer,
  ChecklistCreateSerializer,

  ChecklistNodeListSerializer,
  ChecklistNodeCreateSerializer,

  CheckboxAllowedCoursesListSerializer,
  CheckboxAllowedCoursesCreateSerializer
)


class Admin(BasePermission):
    def has_permission(self, request, view):
      return request.user and request.user.is_staff


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
  """
  ViewSet for MPTT model
  """
  # Prefetch queryset
  queryset = ChecklistNode.objects.select_related(
    # Foreign keys
    'target_checklist',
  ).prefetch_related(
    Prefetch(
      # Reverse foreign keys
      'children', 
      queryset=ChecklistNode.objects.all()
    )
  )
  permission_classes = [Admin]

  def get_serializer_class(self):
    if self.action in ('list', 'retrieve'):
      return ChecklistNodeListSerializer
    elif self.action in ('create', 'update', 'partial_update'):
      return ChecklistNodeCreateSerializer
    return ChecklistNodeListSerializer
  

class CheckboxAllowedCoursesViewSet(ModelViewSet):
  # Prefetch queryset
  queryset = CheckboxAllowedCourses.objects.select_related(
    # Foreign keys
    'target_checkbox',
  ).prefetch_related(
    Prefetch(
      # M2M fields
      'courses', 
      queryset=Course.objects.all()
    )
  )
  permission_classes = [Admin]

  def get_serializer_class(self):
    if self.action in ('list', 'retrieve'):
      return CheckboxAllowedCoursesListSerializer
    elif self.action in ('create', 'update', 'partial_update'):
      return CheckboxAllowedCoursesCreateSerializer
    return CheckboxAllowedCoursesListSerializer
  