from rest_framework.routers import DefaultRouter
from .views import (
  CheckboxAllowedCoursesViewSet, 
  AdditionalConstraintAllowedCoursesViewSet
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

urlpatterns = router.urls