from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.organization_list, name='organization_list'),
    url(r'^(?P<slug>[-\w]+)/$', views.organization_detail,
        name='organization_detail'),
    url(r'^(?P<slug>[-\w]+)/edit/$', views.organization_edit,
        name='organization_edit'),
]