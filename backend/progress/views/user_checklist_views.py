from rest_framework.viewsets import ReadOnlyModelViewSet
from django.db.models import Prefetch
from django_filters.rest_framework import DjangoFilterBackend

from ..models.user_checklist import UserChecklist, UserChecklistNode
from ..serializers.user_checklist_serializers import (
  UserChecklistNodeSerializer,
  UserChecklistDetailSerializer,
)


class UserChecklistViewSet(ReadOnlyModelViewSet):
  # Flexible filtering, searching, and ordering
  filter_backends = [DjangoFilterBackend]
  filterset_fields = {
    'year': ['exact'], 
    'specialization': ['exact'], 
  }

  def get_queryset(self):
    return (
      UserChecklist.objects
      .filter(user=self.request.user)
      .select_related(
        # Foreign keys
        'specialization',
        'original_checklist',
      ).prefetch_related(
        Prefetch(
          # Node
          'nodes',
          queryset=UserChecklistNode.objects
          .filter(parent__isnull=True)
          .select_related(
            # Foreign keys
            'selected_course',
            'original_checkbox',
          ).prefetch_related(
            # Reverse foreign keys
            'children'
          )
        )
      )
    )
  
  def get_serializer_class(self):
    return UserChecklistDetailSerializer
