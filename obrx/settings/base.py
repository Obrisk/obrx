"""
Django settings for obrx project.

Generated by 'django-admin startproject' using Django 3.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""

import logging,os
import sentry_sdk
import requests
from pathlib import Path

from django.utils import timezone
from django.conf import settings
from sentry_sdk.integrations.django import DjangoIntegration

import boto3
import environ
from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


ROOT_DIR = environ.Path(__file__) - 3  # (obrx/obrx/base.py - 3 = obrisk/)
APPS_DIR = ROOT_DIR #ROOT_DIR.path("obrisk")

env = environ.Env()
env.read_env(str(ROOT_DIR.path(".env")))

ALLOWED_HOSTS = ['*']

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True


# INTERNATIONALIZATION
# ------------------------------------------------------------------------------
# Local time zone. Choices are
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# though not all of them may be available with every OS.
# In Windows, this must be set to your system time zone.
TIME_ZONE = "Asia/Chongqing"
# https://docs.djangoproject.com/en/dev/ref/settings/#site-id
SITE_ID = 1
# https://docs.djangoproject.com/en/dev/ref/settings/#use-i18n
USE_I18N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-l10n
USE_L10N = True
# https://docs.djangoproject.com/en/dev/ref/settings/#use-tz
USE_TZ = True

# https://docs.djangoproject.com/en/dev/ref/settings/#language-code
LANGUAGE_CODE = "en-us"

LANGUAGES = (
    ("en", _("English")),
)

LOCALE_PATHS = [
    str(ROOT_DIR.path("locale")),
]

FORM_RENDERER = "django.forms.renderers.TemplatesSetting"

# MIGRATIONS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#migration-modules
MIGRATION_MODULES = {"sites": "obrx.contrib.sites.migrations"}

# https://docs.djangoproject.com/en/dev/ref/settings/#authentication-backends
AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend"
]

SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_AGE = 60 * 60 * 24 * 40  # 40 Days.

# PASSWORDS
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#password-hashers
PASSWORD_HASHERS = [
    # https://docs.djangoproject.com/en/dev/topics/auth/passwords/#using-argon2-with-django
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
    "django.contrib.auth.hashers.BCryptPasswordHasher",
]

# STATIC
# -------------------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#std:setting-STATICFILES_DIRS
STATICFILES_DIRS = [
    str(APPS_DIR.path('static')),
]

# https://docs.djangoproject.com/en/dev/ref/contrib/staticfiles/#staticfiles-finders
STATICFILES_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
]

# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#email-backend
EMAIL_BACKEND = env(
    "EMAIL_BACKEND", default="django.core.mail.backends.smtp.EmailBackend"
)

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
ADMIN_URL = env("ADMIN_URL", default="admin/")

# https://docs.djangoproject.com/en/dev/ref/settings/#admins
ADMINS = [
    ("Elisha Kingdom", "monitor@obrisk.com"),
]
# https://docs.djangoproject.com/en/dev/ref/settings/#managers
MANAGERS = ADMINS

# django-allauth
# ------------------------------------------------------------------------------
# https://django-allauth.readthedocs.io/en/latest/configuration.html
ACCOUNT_ALLOW_REGISTRATION = env.bool("ACCOUNT_ALLOW_REGISTRATION", True)

ACCOUNT_AUTHENTICATION_METHOD = "username_email"

# This is because of overiding login forms on users.forms
# options are False and True for the remember me box
SESSION_REMEMBER = None

ACCOUNT_EMAIL_VERIFICATION = "optional"

SOCIALACCOUNT_EMAIL_VERIFICATION = "none"

# This will avoid the duplicates in usernames with diff casing
ACCOUNT_PRESERVE_USERNAME_CASING = True

ACCOUNT_USERNAME_MIN_LENGTH = 3

ACCOUNT_USERNAME_MAX_LENGTH = 18



ACCOUNT_USERNAME_BLACKLIST = [
    "AnonymousUser",
    "admin",
    "obrisk",
    "password",
    "13300000000",
    "+8613300000000",
    "username",
    "user",
    "god",
    "policeman",
]

ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False

ACCOUNT_LOGIN_ON_PASSWORD_RESET = True

#ACCOUNT_ADAPTER = "obrisk.users.adapters.AccountAdapter"


# Max data to be uploaded to Django server. This is around 1.2GB
DATA_UPLOAD_MAX_MEMORY_SIZE = 1300000000

FILE_UPLOAD_MAX_MEMORY_SIZE = 1300000000

APPEND_SLASH = True
# Name of cache backend to cache user agents. If it not specified default
# cache alias will be used. Set to `None` to disable caching.
# USER_AGENTS_CACHE = 'default'


# REDIS setup
REDIS_URL = f'{env("REDIS_URL", default="redis://127.0.0.1:6379")}/{0}'


# https://docs.djangoproject.com/en/dev/ref/settings/#allowed-hosts
# ALB health check requests should be allowed, whitelist IP address 

# GENERAL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = 'secured-security-8325234'


# DATABASES
# ------------------------------------------------------------------------------
# http://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
    "default": env.db("DATABASE_URL"),
}
DATABASES['default']['ATOMIC_REQUESTS'] = False  # From django-db-geventpool
DATABASES['default']['CONN_MAX_AGE'] = env.int('CONN_MAX_AGE', default=0)  # From django-db-geventpool

# CACHES
# ------------------------------------------------------------------------------

# REDIS setup
REDIS_URL = f'{env("PRIMARY_REDIS_URL", default="redis://127.0.0.1:6379")}/{0}'

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": [
            REDIS_URL,
            #env('SLAVE_REDIS_URL'),
        ],
        "OPTIONS": {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            # Mimicing memcache behavior.
            # http://niwinz.github.io/django-redis/latest/#_memcached_exceptions_behavior
            'IGNORE_EXCEPTIONS': True,
        }
    }
}


# STATIC
# ----------------------------------------------------------------------------

# https://docs.djangoproject.com/en/dev/ref/settings/#static-root
STATIC_ROOT = str(ROOT_DIR('staticfiles'))

STATIC_URL =  '/static/'


# MEDIA
# ------------------------------------------------------------------------------
# The default location for the media files stored in bucket.

OSS_MEDIA_LOCATION = '/media/'

MEDIA_URL = '/media/'


# EMAIL
# ------------------------------------------------------------------------------
# https://docs.djangoproject.com/en/dev/ref/settings/#default-from-email
DEFAULT_FROM_EMAIL = env(
    'DEFAULT_FROM_EMAIL',
    default='Obrisk <notifications@obrisk.com>'
)
# https://docs.djangoproject.com/en/dev/ref/settings/#server-email
SERVER_EMAIL = env('SERVER_EMAIL', default=DEFAULT_FROM_EMAIL)
# https://docs.djangoproject.com/en/dev/ref/settings/#email-subject-prefix
EMAIL_SUBJECT_PREFIX = env('EMAIL_SUBJECT_PREFIX', default='[Obrisk]')

# ADMIN
# ------------------------------------------------------------------------------
# Django Admin URL regex.
ADMIN_URL = env('ADMIN_URL')

#SESSION
#Improve performance #Support multiple servers
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_CACHE_ALIAS = "default"


# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'taggit',
    'wechat_bot',
    'users',
    'classifieds',
    'messager',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'obrx.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(APPS_DIR.path("templates")), ],
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

WSGI_APPLICATION = 'obrx.wsgi.application'


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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


# https://docs.djangoproject.com/en/dev/ref/settings/#auth-user-model
AUTH_USER_MODEL = "users.User"


# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
