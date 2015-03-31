from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'plogs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('plogs.main.urls')),
    url(r'^plane/', include('plogs.planes.urls', namespace='planes', app_name='planes')),
    url(r'^build/', include('plogs.buildlogs.urls', namespace='build', app_name='buildlogs')),
)
