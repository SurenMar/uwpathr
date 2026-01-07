from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class SignUpThrottle(AnonRateThrottle):
  rate = '3/min'

class LoginThrottle(AnonRateThrottle):
  rate = '5/min'

class OAuthThrottle(AnonRateThrottle):
  rate = '5/min'

class TokenRefreshThrottle(AnonRateThrottle):
  rate = '10/min'

class TokenVerifyThrottle(AnonRateThrottle):
  rate = '20/min'

class LogoutThrottle(UserRateThrottle):
  rate = '30/min'

class DeleteAccountThrottle(UserRateThrottle):
  rate = '3/day'
