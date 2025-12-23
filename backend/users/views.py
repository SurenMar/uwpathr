from django.conf import settings
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from djoser.social.views import ProviderAuthView
from rest_framework_simplejwt.views import (
  TokenObtainPairView,
  TokenRefreshView,
  TokenVerifyView
)

class CustomProviderAuthView(ProviderAuthView):
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
        samesite=settings.AUTH_COOKIE_SAME_SITE
      )
      response.set_cookie(
        'refresh', 
        refresh_token,
        max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
        path=settings.AUTH_COOKIE_PATH,
        secure=settings.AUTH_COOKIE_SECURE,
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        samesite=settings.AUTH_COOKIE_SAME_SITE
      )

    # Remove from response body
    response.data.pop("access", None)
    response.data.pop("refresh", None)

    return response

# Override following methods to handle cookies

# Grab tokens from request body and place them in cookies
class CustomTokenObtainPairView(TokenObtainPairView):
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
        samesite=settings.AUTH_COOKIE_SAME_SITE
      )
      response.set_cookie(
        'refresh', 
        refresh_token,
        max_age=settings.AUTH_COOKIE_REFRESH_MAX_AGE,
        path=settings.AUTH_COOKIE_PATH,
        secure=settings.AUTH_COOKIE_SECURE,
        httponly=settings.AUTH_COOKIE_HTTP_ONLY,
        samesite=settings.AUTH_COOKIE_SAME_SITE
      )

    # Remove from response body
    response.data.pop("access", None)
    response.data.pop("refresh", None)

    return response
  

# Grab refresh token from cookies, place in request body, and place the
#   newly generated access token inside cookies
class CustomTokenRefreshView(TokenRefreshView):
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
        samesite=settings.AUTH_COOKIE_SAME_SITE
      )

    # Remove from response body
    response.data.pop("access", None)

    return response


# Grab access token from cookies and place in request body
class CustomTokenVerifyView(TokenVerifyView):
  def post(self, request, *args, **kwargs):
    access_token = request.COOKIES.get('access')

    if access_token:
      request.data['token'] = access_token

    return super().post(request, *args, **kwargs)
  
class LogoutView(APIView):
  def post(self, request, *args, **kwargs):
    response = Response(status=status.HTTP_204_NO_CONTENT)
    response.delete_cookie('access')
    response.delete_cookie('refresh')

    return response


    
