from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication

class CustomJWTAuthentication(JWTAuthentication):
  # Override authenticate to also check for tokens in cookies
  def authenticate(self, request):
    try:
      header = self.get_header(request) # Extracts only auth header (JWTAuth version)
      if header is None:
        raw_token = request.COOKIES.get(settings.AUTH_COOKIE)
      else:
        raw_token = self.get_raw_token(header)

      if raw_token is None:
        return None

      validated_token = self.get_validated_token(raw_token)

      return self.get_user(validated_token), validated_token
    except:
      return None
    