from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
        url(r'^new/$', views.new, name='new'),
)