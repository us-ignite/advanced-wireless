from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.hub_list, name='hub_list'),
    url(r'^apply/$', views.hub_application, name='hub_application'),
    url(r'^(?P<slug>[-\w]+)/$', views.hub_detail, name='hub_detail'),
    url(r'^(?P<slug>[-\w]+)/locations.json$', views.hub_locations_json,
        name='hub_locations_json'),
    url(r'^(?P<slug>[-\w]+)/membership/$', views.hub_membership,
        name='hub_membership'),
    url(r'^(?P<slug>[-\w]+)/membership/remove/$', views.hub_membership_remove,
        name='hub_membership_remove'),
    url(r'^(?P<slug>[-\w]+)/edit/$', views.hub_edit, name='hub_edit'),
]
