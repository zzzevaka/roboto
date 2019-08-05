"""
Django settings for roboto project.

Generated by 'django-admin startproject' using Django 2.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os


def get_config_option(section, option, default=None):
    return os.environ.get("ROBOTO_{}_{}".format(section.upper(), option.upper()), default)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'hmo8w4ie@c9jb@e5mp#w&6llgl$*4j4hvhc-s^^&he%49*b1vy'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = int(get_config_option('GLOBAL', 'debug', 0))

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_extensions',
    'django_celery_beat',
]

PROJECT_APPS = [
    'roboto',
    'oanda',
    'learning',
    'strategy',
    'finam_data',
]

INSTALLED_APPS += PROJECT_APPS

MIDDLEWARE = [
    'rollbar.contrib.django.middleware.RollbarNotifierMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'roboto.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'roboto.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'roboto',
        'USER': 'roboto',
        'PASSWORD': 'password',
        'HOST': 'mysql',
        'PORT': '3306',
        'CONN_MAX_AGE': 0
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

STATIC_URL = '/static/'


#
# Celery
#

REDIS_URL = 'redis://redis:6379/0'

#
# File Storage
#
AWS_S3_CUSTOM_DOMAIN = '127.0.0.1:9000/roboto'
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_S3_ENDPOINT_URL = 'http://minio:9000/'
AWS_ACCESS_KEY_ID = 'development_minio_key'
AWS_SECRET_ACCESS_KEY = 'development_minio_secret'
AWS_STORAGE_BUCKET_NAME = 'roboto'
AWS_S3_FILE_OVERWRITE = False
AWS_S3_SECURE_URLS = False

#
# Error Tracking
#
ROLLBAR = {
    'access_token': get_config_option('ROLLBAR', 'key'),
    'environment': get_config_option('ROLLBAR', 'env'),
    'root': BASE_DIR,
}

#
# Jupyper
#

NOTEBOOK_ARGUMENTS = [
    '--ip', '0.0.0.0',
    '--port', '8888',
    '--notebook-dir', 'notebooks',
    '--allow-root',

]

#
# Learning
#

FEATURE_STORES = [
    'oanda.features',
    'finam_data.features',
]

#
# OANDA
#

OANDA_API_HOST = 'api-fxpractice.oanda.com'
OANDA_API_PORT = 443
OANDA_API_TOKEN = get_config_option('OANDA', 'token')

try:
    from local_settings import *
except ImportError:
    pass

import rollbar
rollbar.init(**ROLLBAR)
