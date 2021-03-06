# MASTER BRANCH settings.py
from .installed_apps import *
from .common import *

# print("Using Production Site")

import os

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL_STATIC_CDN_PATH = os.path.join(
    os.path.dirname(os.path.dirname(BASE_DIR)), 'static_cdn')

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '$SERVER_IPv4_ADDRESS']

ADMINS = (
    # ('Administrator', 'info@admin.email'),
)

MANAGERS = ADMINS

SECRET_KEY = os.environ.get("RFMONITORING_SECRET_KEY")

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        # Or path to database file if using sqlite3.
        'NAME': os.path.join(LOCAL_STATIC_CDN_PATH, 'rfmonitoring.sqlite'),
    }
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # insert your TEMPLATE_DIRS here
            os.path.join(os.path.dirname(__file__), '../templates'),
        ],
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': [
                # Insert your TEMPLATE_CONTEXT_PROCESSORS here or use this
                # list if you haven't customized them:
                'django.contrib.auth.context_processors.auth',
                'django.template.context_processors.debug',
                'django.template.context_processors.i18n',
                'django.template.context_processors.media',
                'django.template.context_processors.static',
                'django.template.context_processors.request',
                'django.template.context_processors.tz',
                'django.contrib.messages.context_processors.messages',
            ],
            'loaders': [
                # insert your TEMPLATE_LOADERS here
                'django.template.loaders.filesystem.Loader',
                'django.template.loaders.app_directories.Loader',
            ]
        },
    },
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

STATIC_URL = '/static/'


STATIC_ROOT = os.path.join(LOCAL_STATIC_CDN_PATH, 'static')  # live cdn AWS S3

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]

MEDIA_ROOT = os.path.join(LOCAL_STATIC_CDN_PATH, 'media')
MEDIA_URL = '/media/'


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.DjangoModelPermissions',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}
