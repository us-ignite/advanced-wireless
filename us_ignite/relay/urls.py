from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.contact_ignite, name='contact_ignite'),
    url(r'^(?P<slug>[-\w]+)/$', views.contact_user, name='contact_user'),
]
