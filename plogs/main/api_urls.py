from django.conf.urls import url
from . import api_views as views

urlpatterns = [
	url(r'^auth/$', views.AuthenticatedCheckView.as_view()),
]
