from rest_framework.routers import DefaultRouter
from courses.views import CourseViewSet, CourseRequisiteNodeViewSet

router = DefaultRouter()
router.register(
  'courses', 
  CourseViewSet, 
  basename='course'
)
router.register(
  'requisites', 
  CourseRequisiteNodeViewSet, 
  basename='requisite'
)

urlpatterns = router.urls
