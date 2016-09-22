from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.resource_list, name='resource_list'),
    url(r'^add/$', views.resource_add, name='resource_add'),
    url(r'^(?P<slug>[-\w]+)/$', views.resource_detail, name='resource_detail'),
    url(r'^(?P<slug>[-\w]+)/edit/$', views.resource_edit, name='resource_edit'),
]
