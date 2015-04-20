from django.conf.urls import patterns, include, url
from django.contrib import admin

app_urls = [
    url(r'^plane/', include('plogs.planes.urls', namespace='planes', app_name='planes')),
    url(r'^build/', include('plogs.buildlogs.urls', namespace='build', app_name='buildlogs')),
]

api_urls = [
    url(r'^', include('plogs.main.api_urls', namespace='api.plogs', app_name='main')),
    url(r'^', include('plogs.planes.api_urls', namespace='api.planes', app_name='planes')),
    url(r'^', include('plogs.buildlogs.api_urls', namespace='api.build', app_name='buildlogs')),
];

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'plogs.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('plogs.main.urls')),
    url(r'^people/(?P<username>\w+)/', include(app_urls)),

    url(r'^api/', include(api_urls)),
)
