import os

from djangoappengine.settings_base import *


SECRET_KEY = '=r-$b*8hglm+858&9t043hlm6-&6-3d3vfc4((7yd0dbrakhvi'

OUR_ROOT = os.path.dirname(os.path.realpath(__file__))

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
    'googleappsauth.middleware.GoogleAuthMiddleware',
    #'hoptoad.middleware.HoptoadNotifierMiddleware',
)


SITE_ID = 1

GOOGLE_OPENID_REALM = 'http://*.hudoracybernetics.com/'
AUTH_PROTECTED_AREAS = '/admin'

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
    'djangoappengine',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.markup',
    'django.contrib.admin',
    'django.contrib.flatpages',
    'djangotoolbox',
    'piston',
    'sanctions',
)

# This test runner captures stdout and associates tracebacks with their
# corresponding output. Helps a lot with print-debugging.
TEST_RUNNER = 'djangotoolbox.test.CapturingTestSuiteRunner'

AUTHENTICATION_BACKENDS = ('googleappsauth.backends.GoogleAuthBackend',
                           'django.contrib.auth.backends.ModelBackend',)

# Activate django-dbindexer if available
try:
    import dbindexer
    DATABASES['native'] = DATABASES['default']
    DATABASES['default'] = {'ENGINE': 'dbindexer', 'TARGET': 'native'}
    INSTALLED_APPS += ('dbindexer',)
except ImportError:
    pass