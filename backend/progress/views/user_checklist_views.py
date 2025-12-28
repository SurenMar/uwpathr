from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend

from progress.models.user_checklist import UserChecklist, UserChecklistNode
from progress.serializers.user_checklist_serializers import (
  UserChecklistDetailSerializer,
  UserChecklistCreateSerializer,
  UserChecklistNodeUpdateSerializer,
)


class UserChecklistViewSet(ReadOnlyModelViewSet, CreateModelMixin):
  filter_backends = [DjangoFilterBackend]
  filterset_fields = {
    'year': ['exact'], 
    'specialization': ['exact'], 
  }

  # Recursively get the nodes (requirements) for the head (checklist)
  def get_queryset(self):
    return (
      UserChecklist.objects
      .filter(user=self.request.user)
      .select_related(
        'specialization',
        'original_checklist',
      ).prefetch_related(
        Prefetch(
          'nodes',
          queryset=UserChecklistNode.objects
          .select_related(
            'selected_course',
            'original_checkbox',
          ).prefetch_related(
            'children'
          )
        )
      )
    )
  
  def get_serializer_class(self):
    if self.action == 'create':
      return UserChecklistCreateSerializer
    return UserChecklistDetailSerializer
  
  def perform_create(self, serializer):
    serializer.save()


class UserChecklistNodeViewSet(GenericViewSet, UpdateModelMixin):
  serializer_class = UserChecklistNodeUpdateSerializer
  http_method_names = ['patch']

  def get_queryset(self):
    return UserChecklistNode.objects.filter(user=self.request.user)
  
  def perform_create(self, serializer):
    serializer.save(user=self.request.user)
