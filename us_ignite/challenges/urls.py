from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.challenge_list, name='challenge_list'),
    url(r'^(?P<slug>[-\w]+)/$', views.challenge_detail, name='challenge_detail'),
    url(r'^(?P<challenge_slug>[-\w]+)/enter/(?P<app_slug>[-\w]+)/$',
        views.challenge_entry, name='challenge_entry'),
    url(r'^(?P<challenge_slug>[-\w]+)/(?P<app_slug>[-\w]+)/$',
        views.entry_detail, name='entry_detail'),
]
