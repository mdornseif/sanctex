from django.conf.urls.defaults import *
from django.conf import settings
from sanctions.models import Entity


import dbindexer
dbindexer.autodiscover()


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

info_dict = {
    'queryset': Entity.objects.all(),
}

urlpatterns = patterns('',
    (r'^callback_googleappsauth/', 'googleappsauth.views.callback'),
    (r'^admin/', include(admin.site.urls)),
    url(r'download/$', 'sanctions.views.download', name='download'),
    url(r'import-sanctions/$', 'sanctions.views.import_sanctions', name='import-sanctions'),
    (r'api/', include('api.urls')),

    (r'^entity/(?P<object_id>\d+)/', 'django.views.generic.list_detail.object_detail', info_dict),
    (r'^search/', 'sanctions.views.search'),
    (r'^hintergrund/', 'django.views.generic.simple.direct_to_template', {'template': 'sanctions/hintergrund.html'}),
    (r'^how/', 'django.views.generic.simple.direct_to_template', {'template': 'sanctions/how.html'}),
    (r'^$', 'django.views.generic.simple.direct_to_template', {'template': 'sanctions/index.html'}),
)
