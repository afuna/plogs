from django.conf.urls import patterns, url, include
from . import views

urlpatterns = patterns('',
        url(r'^photo_upload_url/$', views.photo_upload_url, name='photo_upload_url'),
        url(r'^partners/$', views.PartnerList.as_view(), name='partner_list'),
        url(r'^partners/new/$', views.PartnerNew.as_view(), name='partner_new'),

        url(r'^new/$', views.BuildLogNew.as_view(), name='new'),
        url(r'^(?P<log_id>\d+)/', include(patterns('',
            url(r'^$', views.BuildLogDetail.as_view(), name='view'),
            url(r'^edit/$', views.BuildLogUpdate.as_view(), name='edit'),
        ))),
)