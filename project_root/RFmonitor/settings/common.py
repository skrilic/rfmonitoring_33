
TIME_ZONE = 'Europe/Paris'

LANGUAGE_CODE = 'en-us'

LANGUAGES = [
    ('en-US', 'English'),
    ('hr-HR', 'Hrvatski'),
]

SITE_ID = 1

USE_I18N = True

USE_L10N = True

MIDDLEWARE = [
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware'
]

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
CSRF_COOKIE_HTTPONLY = True
# X_FRAME_OPTIONS='DENY'
SECURE_CONTENT_TYPE_NOSNIFF = False
SECURE_BROWSER_XSS_FILTER = False
SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0

def custom_show_toolbar():
    return True  # Always show toolbar, for example purposes only.


ROOT_URLCONF = 'RFmonitor.urls'

