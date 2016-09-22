from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.awt_frontpage, name='awt_frontpage'),
    url(r'^awt_default_subscribe/$', views.awt_default_subscribe, name='awt_default_subscribe'),
]
