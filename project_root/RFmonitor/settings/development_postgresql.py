# MASTER BRANCH dev_settings.py
from .installed_apps import *
from .common import *

# print("Using PostgreSQL Development Site")

import os

SITE_ROOT = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOCAL_STATIC_CDN_PATH = os.path.join(
    os.path.dirname(os.path.dirname(BASE_DIR)), 'static_cdn')

DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1', 'localhost', '$SERVER_IPv4_ADDRESS']

ADMINS = (
    # ('Slaven Krilic', 'skrilic@gmail.com'),
)

MANAGERS = ADMINS

SECRET_KEY = '+%-16!s7xdyp1*h$#ck(%#)y_=n49+t0784d^6hlpd%cap!he7'

DATABASES = {
    'default': {
        'NAME': 'rfdjango',
        'ENGINE': 'django.db.backends.postgresql',
        'USER': 'rfdjango',
        'PASSWORD': '123abcQW'
    },
    # 'legacy': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(LOCAL_STATIC_CDN_PATH, 'dev_monitoring.sqlite'),
    # },
    # 'users': {
    #     'NAME': 'user_data',
    #     'ENGINE': 'django.db.backends.mysql',
    #     'USER': 'mysql_user',
    #     'PASSWORD': 'priv4te'
    # }
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

STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(LOCAL_STATIC_CDN_PATH, "static"),
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
)

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(LOCAL_STATIC_CDN_PATH, "media")

APPEND_SLASH = False
# OLWIDGET Dependancy
# YAHOO_APP_ID='XYZ'
# CLOUDMADE_API_KEY='XYZ'
# GOOGLE_API_KEY='XYZ' #(no key is required for low request volumes).

EXCEL_SUPPORT = 'xlwt'


# LEAFLET_CONFIG = {
#     #'SPATIAL_EXTENT': (17.8, 40.0, 20.8, 45.0),
#     'DEFAULT_CENTER': (44.0, 17.8),
#     'DEFAULT_ZOOM': 8,
#     'MIN_ZOOM': 3,
#     'MAX_ZOOM': 18,
#     'SCALE': 'metric',
#     'MINIMAP': False,
#     'RESET_VIEW': False
# }

# Must be enabled in installed_apps.py
REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    # 'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly',),
    'DEFAULT_PERMISSION_CLASSES': ('rest_framework.permissions.DjangoModelPermissions',),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100
}