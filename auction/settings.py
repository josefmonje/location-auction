"""
Django settings for auction project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""
import os
import dj_database_url

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SECRET_KEY = '+lf6xllk2gw2=0*c$8w%57k$p43fkqk#_&9ho8fyf(0(%mc1pe'

DEBUG = True
TEMPLATE_DEBUG = True

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.gis',
    'auction',
    'djgeojson',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'auction.urls'

WSGI_APPLICATION = 'auction.wsgi.application'

local = False

if local is True:
    DATABASES = {
        'default': {
            # 'ENGINE': 'django.db.backends.postgresql_psycopg2',
            # https://docs.djangoproject.com/en/1.7/ref/contrib/gis/install/postgis/
            # create extension postgis; sql in database
            'ENGINE': 'django.contrib.gis.db.backends.postgis',
            'NAME': 'auction',
            'USER': 'postgres',
            'PASSWORD': 'password',
            'HOST': 'localhost',
            'PORT': '',
        }
    }
    GEOS_LIBRARY_PATH = 'C:\\OSGeo4W64\\bin\\geos_c.dll'
    POSTGIS_VERSION = (2, 0, 3)  # / (1, 5, 2)
else:
    DATABASES = {}
    DATABASES['default'] = dj_database_url.config(
        default='postgres://evrmrzgismhlpy:cNoLb67sD2Hm8Ni16aMRac3LIZ@ec2-107-20-244-236.compute-1.amazonaws.com:5432/d2t8p76nm2udn6')

LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/London'
USE_I18N = True
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATIC_ROOT = 'staticfiles'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

TEMPLATE_DIRS = (
    os.path.join(BASE_DIR, 'templates'),
)

SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
ALLOWED_HOSTS = ['*']
STATICFILES_STORAGE = 'whitenoise.django.GzipManifestStaticFilesStorage'
