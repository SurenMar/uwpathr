from rest_framework.routers import DefaultRouter
from courses.views import CourseViewSet, CoursePrerequisiteNodeViewSet

router = DefaultRouter()
router.register(
  'courses', 
  CourseViewSet, 
  basename='course'
)
router.register(
  'courses/prerequisites', 
  CoursePrerequisiteNodeViewSet, 
  basename='course-prerequisite'
)

urlpatterns = router.urls
