from django.conf.urls.defaults import *
from django.conf import settings


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    ('^admin/', include(admin.site.urls)),
    url(r'download/$', 'sanctions.views.download', name='download'),
    (r'^search/', 'sanctions.views.search'),
    (r'api/', include('api.urls')),
   
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
         'document_root': settings.BASEDIR + '/media' }
      ),
      
     (r'^$', 'sanctions.views.index'),
)
