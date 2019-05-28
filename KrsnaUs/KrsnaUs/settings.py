"""
Django settings for KrsnaUs project.

Generated by 'django-admin startproject' using Django 1.11.4.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
from types import SimpleNamespace

try:
    import config
except ImportError:
    config = SimpleNamespace(
        SECRET_KEY='default_key',
        POSTGRES_DB='default_db',
        POSTGRES_USER='postgres',
        POSTGRES_PASSWORD='password',
        PSG_HOST='localhost',
        PSG_PORT=5432,
        ES_NAME='elastic',
        ELASTIC_PASSWORD='password',
        DEBUG=True,
        EMAIL_USER='default_email',
        EMAIL_PASS='password',
        CLIENT_URL='http://localhost:3000'
    )

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY', config.SECRET_KEY)

# SECURITY WARNING: don't run with debug turned on in production!
debug_str = os.getenv('DEBUG', config.DEBUG)
DEBUG = debug_str if type(debug_str) == bool else debug_str == 'True'

ALLOWED_HOSTS = ['localhost', '.gvparchives.com', 'krsnaus', '192.168.0.11', "*"]

AUTH_USER_MODEL = 'harikatha.User'

# Application definition

CLIENT_URL = os.getenv('CLIENT_URL', config.CLIENT_URL)

DEV_BACKEND = 'django.core.mail.backends.console.EmailBackend'
PROD_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_BACKEND = DEV_BACKEND if DEBUG else PROD_BACKEND
EMAIL_HOST = os.getenv('EMAIL_HOST', 'smtp.gmail.com')
EMAIL_PORT = 587
EMAIL_HOST_USER = os.getenv('EMAIL_USER', config.EMAIL_USER)
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_PASS', config.EMAIL_PASS)
EMAIL_USE_TLS = True
EMAIL_SSL = False
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

SOCIALACCOUNT_EMAIL_VERIFICATION = False
OLD_PASSWORD_FIELD_ENABLED = True
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = "email"
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_CONFIRMATION_COOLDOWN = 20
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'https'

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'rest_framework',
    'rest_auth',
    'allauth',
    'allauth.account',
    'rest_auth.registration',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'corsheaders',
    'rest_framework.authentication',
    'rest_framework.authtoken',
    'harikatha.apps.HarikathaConfig',
]

REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.IsAdminUser',
    # ],
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        # 'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'harikatha.pagination.CustomPagination',
    'PAGE_SIZE': 20
    # 'PAGE_SIZE': 10
}

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True

ROOT_URLCONF = 'KrsnaUs.urls'
SITE_ID = 1
# REST_SESSION_LOGIN = True

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,  'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'KrsnaUs.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('POSTGRES_DB', config.POSTGRES_DB),
        'USER': os.getenv('POSTGRES_USER', config.POSTGRES_USER),
        'PASSWORD': os.getenv('POSTGRES_PASSWORD', config.POSTGRES_PASSWORD),
        'HOST': os.getenv('PSG_HOST', config.PSG_HOST),
        'PORT': os.getenv('PSG_PORT', config.PSG_PORT)
    }
}

AUTHENTICATION_BACKENDS = (
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by e-mail
    'allauth.account.auth_backends.AuthenticationBackend',
)


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = os.getenv('STATIC_URL', '/static/')
STATIC_ROOT = '/static/'
