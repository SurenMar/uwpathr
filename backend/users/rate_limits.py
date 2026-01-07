from rest_framework.throttling import AnonRateThrottle, UserRateThrottle

class SignUpThrottle(AnonRateThrottle):
  scope = 'signup'
  rate = '3/min'

class LoginThrottle(AnonRateThrottle):
  scope = 'login'
  rate = '5/min'

class OAuthThrottle(AnonRateThrottle):
  scope = 'oauth_login'
  rate = '5/min'

class TokenRefreshThrottle(AnonRateThrottle):
  scope = 'token_refresh'
  rate = '10/min'

class TokenVerifyThrottle(AnonRateThrottle):
  scope = 'token_verify'
  rate = '20/min'

class LogoutThrottle(UserRateThrottle):
  scope = 'logout'
  rate = '30/min'

class DeleteAccountThrottle(UserRateThrottle):
  scope = 'delete_account'
  rate = '3/day'
