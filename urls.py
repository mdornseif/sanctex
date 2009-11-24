from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^sanction_names/', include('sanction_names.foo.urls')),
    url(r'download/$', 'sanctions.views.download', name='download'),
    (r'^api/', include('api.urls')),
    (r'$', 'sanctions.views.search'),
)
