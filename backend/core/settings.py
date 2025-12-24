from os import getenv, path
from pathlib import Path
from django.core.management.utils import get_random_secret_key
import dotenv

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

dotenv_file = BASE_DIR / '.env.local'

if path.isfile(dotenv_file):
  dotenv.load_dotenv(dotenv_file)

SECRET_KEY = getenv('DJANGO_SECRET_KEY', get_random_secret_key())
DEBUG = getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = getenv('DJANGO_ALLOWED_HOSTS', 
                       '127.0.0.1,localhost').split(',')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.postgres',
    'corsheaders',
    'mptt',                         # For tree like models
    'treebeard',                    # For tree like models
    'rest_framework',
    'django_filters',               # For API filtering
    'djoser',                       # For authentication
    'checklists',
    'courses',
    'progress',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'


# Database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': getenv('DB_NAME'),
        "USER": getenv('DB_USER'),
        "PASSWORD": getenv('DB_PASSWORD'),
        'HOST': getenv('DB_HOST'),
        'PORT': getenv('DB_PORT'),
    }
}


# Email settings

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'surepic342@gmail.com'

# EMAIL_BACKEND = 'django_ses.SESBackend'
# AWS_SES_ACCESS_KEY_ID = getenv('AWS_SES_ACCESS_KEY_ID')
# AWS_SES_SECRET_ACCESS_KEY_ID = getenv('AWS_SES_SECRET_ACCESS_KEY_ID')
# USE_SES_V2 = True

# AWS_SES_REGION_NAME = getenv('AWS_SES_REGION_NAME')
# AWS_SES_REGION_ENDPOINT = f'email.{AWS_SES_REGION_NAME}.amazonaws.com'
# AWS_SES_FROM_EMAIL = getenv('AWS_SES_FROM_EMAIL')
# DEFAULT_FROM_EMAIL = getenv('AWS_SES_FROM_EMAIL') # Used by djoser

DOMAIN = getenv('DOMAIN')
SITE_NAME = 'UWPathr'


# Password

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
]


# Internationalization

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'
MEDIA_URL = 'media/' 
MEDIA_ROOT = BASE_DIR / 'media'

REST_FRAMEWORK = {
  'DEFAULT_AUTHENTICATION_CLASSES': [
    'users.authentication.CustomJWTAuthentication',
  ],
  'DEFAULT_PERMISSION_CLASSES': [
    'rest_framework.permissions.IsAuthenticated',
  ],
  'DEFAULT_THROTTLE_CLASSES': [
      'rest_framework.throttling.AnonRateThrottle',
      'rest_framework.throttling.UserRateThrottle',
    ],
    'DEFAULT_THROTTLE_RATES': {
      'anon': '100/min',
      'user': '1000/min',
    },
}

DJOSER = {
#   'PASSWORD_RESET_CONFIRM_URL': 'password-reset/{uid}/{token}',
#   'SEND_ACTIVATION_EMAIL': True,
#   'ACTIVATION_URL': 'activation/{uid}/{token}',
  'USER_CREATE_PASSWORD_RETYPE': True,
  'SET_PASSWORD_RETYPE': True,
  'PASSWORD_RESET_CONFIRM_RETYPE': True,
  'TOKEN_MODEL': None,
  #'SOCIAL_AUTH_ALLOWED_REDIRECT_URIS': getenv('REDIRECT_URLS').split(',')
}

AUTH_COOKIE = 'access'
AUTH_COOKIE_ACCESS_MAX_AGE = 60 * 5 # 5 minutes
AUTH_COOKIE_REFRESH_MAX_AGE = 60 * 60 * 24 # 1 day
AUTH_COOKIE_SECURE = getenv('AUTH_COOKIE_SECURE', 'True') == 'True'
AUTH_COOKIE_HTTP_ONLY = True
AUTH_COOKIE_PATH = '/'
AUTH_COOKIE_SAME_SITE = 'None'

CORS_ALLOWED_ORIGINS = getenv(
  'CORS_ALLOWED_ORIGINS', 
  'http://localhost:3000,http://127.0.0.1:3000'
).split(',')
CORS_ALLOW_CREDENTIALS = True

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.UserAccount'
