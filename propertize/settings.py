import os
import sys
from pathlib import Path

import dj_database_url
import cloudinary
from decouple import config

# ------------------------------------------------------------------------------
# BASE / ENVIRONMENT
# ------------------------------------------------------------------------------

# if you have an env.py in project root, this will load it:
if os.path.isfile('env.py'):
    import env

# Pull in Cloudinary’s single-string URL from .env
CLOUDINARY_URL = config('CLOUDINARY_URL', default='')

# Feed it into the Cloudinary SDK and django-cloudinary-storage
if CLOUDINARY_URL:
    os.environ['CLOUDINARY_URL'] = CLOUDINARY_URL

# Let cloudinary-lib read CLOUDINARY_URL itself; no need for explicit cloudinary.config(...)
# cloudinary.config(secure=True)  # optional, to force https

# ------------------------------------------------------------------------------
# PATHS
# ------------------------------------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
TEMPLATES_DIR = BASE_DIR / 'templates'

# ------------------------------------------------------------------------------
# SECURITY
# ------------------------------------------------------------------------------

SECRET_KEY = config('SECRET_KEY')
DEBUG      = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = ['127.0.0.1', '.herokuapp.com']

# ------------------------------------------------------------------------------
# APPLICATIONS
# ------------------------------------------------------------------------------

INSTALLED_APPS = [
    # Django core
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',

    # Third-party
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'crispy_bootstrap4',
    'django_tables2',
    'django_filters',
    'django_celery_beat',
    'django_celery_results',
    'cloudinary_storage',
    'cloudinary',

    # Your apps
    'users',
    'dashboards',
    'properties',
    'tenants',
    'maintenance',
    'finance',
]

SITE_ID = 1

# ------------------------------------------------------------------------------
# MIDDLEWARE & URLS
# ------------------------------------------------------------------------------

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
]

ROOT_URLCONF = 'propertize.urls'

# ------------------------------------------------------------------------------
# TEMPLATES
# ------------------------------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [str(TEMPLATES_DIR)],
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

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = ['bootstrap4']
CRISPY_TEMPLATE_PACK = 'bootstrap4'

# ------------------------------------------------------------------------------
# WSGI
# ------------------------------------------------------------------------------

WSGI_APPLICATION = 'propertize.wsgi.application'

# ------------------------------------------------------------------------------
# DATABASE
# ------------------------------------------------------------------------------

DATABASES = {
    'default': dj_database_url.parse(
        config('DATABASE_URL', default=f"sqlite:///{BASE_DIR / 'db.sqlite3'}")
    )
}

if 'test' in sys.argv:
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'

# ------------------------------------------------------------------------------
# AUTH & ALLAUTH
# ------------------------------------------------------------------------------

AUTH_USER_MODEL = 'users.CustomUser'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

LOGIN_REDIRECT_URL  = '/'
LOGOUT_REDIRECT_URL = '/'

ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_EMAIL_REQUIRED     = True
ACCOUNT_LOGOUT_ON_GET      = True
ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_FORMS = {
    'signup': 'users.forms.CustomSignupForm',
}

# ------------------------------------------------------------------------------
# EMAIL (local dev writes to files)
# ------------------------------------------------------------------------------

EMAIL_BACKEND  = config('EMAIL_BACKEND',  default='django.core.mail.backends.filebased.EmailBackend')
EMAIL_FILE_PATH = config('EMAIL_FILE_PATH', default=str(BASE_DIR / 'sent_emails'))

# ------------------------------------------------------------------------------
# INTERNATIONALIZATION
# ------------------------------------------------------------------------------

LANGUAGE_CODE = 'en-us'
TIME_ZONE     = 'UTC'
USE_I18N      = True
USE_TZ        = True

# ------------------------------------------------------------------------------
# STATIC & MEDIA
# ------------------------------------------------------------------------------

STATIC_URL         = '/static/'
STATICFILES_DIRS   = [BASE_DIR / 'static']
STATIC_ROOT        = BASE_DIR / 'staticfiles'

MEDIA_URL          = '/media/'
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# ------------------------------------------------------------------------------
# CSRF
# ------------------------------------------------------------------------------

CSRF_TRUSTED_ORIGINS = [
    "http://127.0.0.1",
    "https://*.herokuapp.com"
]

# ------------------------------------------------------------------------------
# CELERY
# ------------------------------------------------------------------------------

CELERY_RESULT_BACKEND = 'django-db'
CELERY_BROKER_URL     = config('REDIS_TLS_URL', default=os.environ.get('REDIS_URL'))
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers.DatabaseScheduler'

# ------------------------------------------------------------------------------
# OTHER DEFAULTS
# ------------------------------------------------------------------------------

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
handler404 = 'users.views.custom404'
