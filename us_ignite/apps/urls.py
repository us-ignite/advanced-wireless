from django.conf.urls import  url
from . import views


urlpatterns = [
    url(r'^$', views.app_list, name='app_list'),
    url(r'^add/$', views.app_add, name='app_add'),
    url(r'^featured/$', views.apps_featured, name='apps_featured'),
    url(r'^featured/archive/(?P<slug>[-\w]+)/$', views.apps_featured_archive,
        name='apps_featured_archive'),
    url(r'^(?P<slug>[-\w]+)/$', views.app_detail, name='app_detail'),
    url(r'^(?P<slug>[-\w]+)/edit/$', views.app_edit, name='app_edit'),
    url(r'^(?P<slug>[-\w]+)/export/$', views.app_export, name='app_export'),
    url(r'^(?P<slug>[-\w]+)/hubs-membership/$', views.app_hub_membership,
        name='app_hub_membership'),
    url(r'^(?P<slug>[-\w]+)/membership/$', views.app_membership,
        name='app_membership'),
    url(r'^domain/(?P<domain>[-\w]+)/$', views.app_list, name='app_list_domain'),
    url(r'^stage/(?P<stage>[\d]{1})/$', views.app_list, name='app_list_stage'),
]
