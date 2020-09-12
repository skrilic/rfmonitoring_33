from installed_apps import *
from common import *

import os

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# BASE_DIR = '/home/slaven/projects/rfmonitoring_33/project_root'
LOCAL_STATIC_CDN_PATH = os.path.join(
    os.path.dirname(os.path.dirname(BASE_DIR)), 'static_cdn')

DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'localhost',
                 'rfdjango.planone.site', '$SERVER_IPv4_ADDRESS']

ADMINS = (
    # ('Slaven Krilic', 'skrilic@gmail.com'),
)

MANAGERS = ADMINS

SECRET_KEY = os.environ.get(
    "SECRET_KEY", '+%-16!s7xdyp1*h$#ck(%#)y_=n49+t0784d^6hlpd%cap!he7')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        # Or path to database file if using sqlite3.
        # 'NAME': os.path.join(LOCAL_STATIC_CDN_PATH, 'monitoring.sqlite'),
        'NAME': '/var/opt/rfmonitoring/static_cdn/monitoring.sqlite',
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
    os.path.join(LOCAL_STATIC_CDN_PATH, 'static')
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
