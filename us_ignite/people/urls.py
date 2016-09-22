from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.profile_list, name='profile_list'),
    url(r'^(?P<slug>[-_\w]{1,32})/$', views.profile_detail, name='profile_detail'),
]
