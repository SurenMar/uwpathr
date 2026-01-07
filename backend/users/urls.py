from rest_framework.routers import DefaultRouter
from django.urls import path, re_path
from users.views import *

router = DefaultRouter()
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
  re_path(
    r'^o/(?P<provider>\S+)/$',
    CustomProviderAuthView.as_view(),
    name='provider_auth'
  ),
  path('jwt/create/', CustomTokenObtainPairView.as_view()),
  path('jwt/refresh/', CustomTokenRefreshView.as_view()),
  path('jwt/verify/', CustomTokenVerifyView.as_view()),
  path('logout/', LogoutView.as_view()),
  path('delete-account/', DeleteAccountView.as_view()),
]
