import os, sys, site

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
site.addsitedir(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'pythonenv/lib/python2.6/site-packages'))

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()