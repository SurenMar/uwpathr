from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views

router = DefaultRouter()
router.register('courses', views.CourseViewSet)

urlpatterns = [
  path('api/', include(router.urls)),
]
