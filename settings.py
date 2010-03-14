# Django settings for sanction_names project.
import os

import os
import django

from cs.global_django_settings import *

#ADMIN_MEDIA_PREFIX = 'http://s.hdimg.net/djangoadmin/1.0.2/'

OUR_ROOT = os.path.dirname(os.path.realpath(__file__))

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'googleappsauth.middleware.GoogleAuthMiddleware',
    'hoptoad.middleware.HoptoadNotifierMiddleware',
)

DEBUG = True
if os.environ.get('SILVER_VERSION', '').startswith('silverlining/'):
    # we are running on a silverlining manages production server.
    # see http://cloudsilverlining.org/services.html#silver-version-environmental-variable
    DEBUG = False
TEMPLATE_DEBUG = DEBUG
TEMPLATE_STRING_IF_INVALID = " #_%s_# "

MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3' # 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
DATABASE_NAME = os.path.join(os.environ['CONFIG_FILES'], 'django.db')
DATABASE_USER = 'root'                # Not used with sqlite3.
#DATABASE_PASSWORD = 'djangopass'        # Not used with sqlite3.
DATABASE_HOST = ''             # Set to empty string for localhost. Not used with sqlite3.
DATABASE_PORT = ''             # Set to empty string for default. Not used with sqlite3.

SITE_ID = 1
GOOGLE_OPENID_REALM = 'http://*.hudoracybernetics.com/'
AUTH_PROTECTED_AREAS = '/admin'
HOPTOAD_API_KEY = '34a6b7ed9e6d9b50b3c910233263c91b'
HOPTOAD_NOTIFY_404 = True
HOPTOAD_NOTIFY_403 = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://media.lawrence.com", "http://example.com/media/"
MEDIA_URL = ''

ROOT_URLCONF = 'urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(OUR_ROOT, 'generic_templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.markup',
    'django.contrib.admin',
    'django.contrib.flatpages',
    #'hudjango',
    'piston',
    'sanctions',
 )

AUTHENTICATION_BACKENDS = ('googleappsauth.backends.GoogleAuthBackend', 
                           'django.contrib.auth.backends.ModelBackend',)
