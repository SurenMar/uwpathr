from rest_framework.routers import DefaultRouter
from progress.views.user_checklist_views import (
  UserChecklistViewSet, 
  UserChecklistNodeViewSet
)
from .views.user_course_views import (
  UserCourseViewSet,
  UserPathNodeViewSet,
)
from .views.user_requirements_views import (
  UserAdditionalConstraintViewSet,
  UserDepthListViewSet
)

router = DefaultRouter()
router.register(
  'user-checklists', 
  UserChecklistViewSet, 
  basename='user-checklist'
)
router.register(
  'user-checklist-nodes', 
  UserChecklistNodeViewSet, 
  basename='user-checklist-node'
)
router.register(
  'user-courses', 
  UserCourseViewSet, 
  basename='user-course'
)
router.register(
  'user-path-nodes', 
  UserPathNodeViewSet, 
  basename='user-path-node'
)
router.register(
  'user-additional-constraints', 
  UserAdditionalConstraintViewSet, 
  basename='user-additional-constraint'
)
router.register(
  'user-depth-lists', 
  UserDepthListViewSet, 
  basename='user-depth-list'
)

urlpatterns = router.urls
