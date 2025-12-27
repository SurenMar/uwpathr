from rest_framework.routers import DefaultRouter
from checklists.views import (
  CheckboxAllowedCoursesViewSet, 
  AdditionalConstraintAllowedCoursesViewSet,
  SpecializationViewSet,
) 

router = DefaultRouter()
router.register(
  'checkbox-allowed-courses', 
  CheckboxAllowedCoursesViewSet, 
  basename='checkbox-allowed-course')
router.register(
  'additional-constraint-allowed-courses', 
  AdditionalConstraintAllowedCoursesViewSet, 
  basename='additional-constraint-allowed-course')
router.register(
  'specializations',
  SpecializationViewSet,
  basename='specialization'
)

urlpatterns = router.urls