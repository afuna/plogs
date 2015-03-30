from django.conf.urls import patterns, url

from . import views

urlpatterns = patterns('',
        url(r'^signup/$', views.signup, name='signup'),
        url(r'^login/$', 'django.contrib.auth.views.login', name='login'),
        url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
        url(r'^$', views.index, name='frontpage'),
)