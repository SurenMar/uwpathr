from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from users.rate_limits import *
from djoser.views import UserViewSet
from djoser.social.views import ProviderAuthView
from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView,
  TokenVerifyView
)


class CustomUserViewSet(UserViewSet):
  def get_throttles(self):
    if self.action == 'create':  # POST /users/
      return [SignUpThrottle()]
    return super().get_throttles()


# OAuth endpoint
class CustomProviderAuthView(ProviderAuthView):
  throttle_classes = [OAuthThrottle]
  def post(self, request, *args, **kwargs):
    response = super().post(request, *args, **kwargs)

    if response.status_code == 201:
      access_token = response.data.get('access')
      refresh_token = response.data.get('refresh')

      response.set_cookie(
        'access', 
        access_token,
        max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
        path=settings.AUTH_COOKIE_PATH,
        secure=settings.AUTH_COOKIE_SECURE,
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        samesite=settings.AUTH_COOKIE_SAMESITE
      )
      response.set_cookie(
        'refresh', 
        refresh_token,
        max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
        path=settings.AUTH_COOKIE_PATH,
        secure=settings.AUTH_COOKIE_SECURE,
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        samesite=settings.AUTH_COOKIE_SAMESITE
      )

    # TODO Remove from response body
    response.data.pop("access", None)
    response.data.pop("refresh", None)

    return response


# Grab tokens from request body and place them in cookies
class CustomTokenObtainPairView(TokenObtainPairView):
  throttle_classes = [LoginThrottle]
  def post(self, request, *args, **kwargs):
    response = super().post(request, *args, **kwargs)

    if response.status_code == 200:
      access_token = response.data.get('access')
      refresh_token = response.data.get('refresh')

      response.set_cookie(
        'access', 
        access_token,
        max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
        path=settings.AUTH_COOKIE_PATH,
        secure=settings.AUTH_COOKIE_SECURE,
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        samesite=settings.AUTH_COOKIE_SAMESITE
      )
      response.set_cookie(
        'refresh', 
        refresh_token,
        max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
        path=settings.AUTH_COOKIE_PATH,
        secure=settings.AUTH_COOKIE_SECURE,
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        samesite=settings.AUTH_COOKIE_SAMESITE
      )

    # TODO Remove from response body
    response.data.pop("access", None)
    response.data.pop("refresh", None)

    return response
  

# Grab refresh token from cookies, place in request body, and place the
#   newly generated access token inside cookies
class CustomTokenRefreshView(TokenRefreshView):
  throttle_classes = [TokenRefreshThrottle]
  def post(self, request, *args, **kwargs):
    refresh_token = request.COOKIES.get('refresh')

    if refresh_token:
      request.data['refresh'] = refresh_token

    response = super().post(request, *args, **kwargs)

    if response.status_code == 200:
      access_token = response.data.get('access')

      response.set_cookie(
        'access', access_token,
        max_age=settings.AUTH_COOKIE_ACCESS_MAX_AGE,
        path=settings.AUTH_COOKIE_PATH,
        secure=settings.AUTH_COOKIE_SECURE,
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        samesite=settings.AUTH_COOKIE_SAMESITE
      )

    # TODO Remove from response body
    response.data.pop("access", None)

    return response


# Grab access token from cookies and place in request body
class CustomTokenVerifyView(TokenVerifyView):
  throttle_classes = [TokenVerifyThrottle]
  def post(self, request, *args, **kwargs):
    access_token = request.COOKIES.get('access')

    if access_token:
      request.data['token'] = access_token

    return super().post(request, *args, **kwargs)
  
class LogoutView(APIView):
  throttle_classes = [LogoutThrottle]
  def post(self, request, *args, **kwargs):
    response = Response(status=status.HTTP_204_NO_CONTENT)
    response.delete_cookie('access')
    response.delete_cookie('refresh')

    return response


class DeleteAccountView(APIView):
  throttle_classes = [DeleteAccountThrottle]
  def delete(self, request, *args, **kwargs):
    user = request.user
    user.delete()
    
    response = Response(status=status.HTTP_204_NO_CONTENT)
    response.delete_cookie('access')
    response.delete_cookie('refresh')
    
    return response
