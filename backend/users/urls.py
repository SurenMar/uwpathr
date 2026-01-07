from djoser.urls import router
from django.urls import path, re_path
from users.views import *

router.registry.clear()
router.register('users', CustomUserViewSet, basename='users')

urlpatterns = [
  re_path(
    r'^o/(?P<provider>\S+)/$',
    CustomProviderAuthView.as_view(),
    name='provider_auth'
  ),
  path('users/', CustomUserViewSet.as_view()),
  path('jwt/create/', CustomTokenObtainPairView.as_view()),
  path('jwt/refresh/', CustomTokenRefreshView.as_view()),
  path('jwt/verify/', CustomTokenVerifyView.as_view()),
  path('logout/', LogoutView.as_view()),
  path('delete-account/', DeleteAccountView.as_view()),
]
