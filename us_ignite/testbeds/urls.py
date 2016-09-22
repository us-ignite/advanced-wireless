from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.testbed_list, name='testbed_list'),
    url(r'^(?P<slug>[-\w]+)/$', views.testbed_detail, name='testbed_detail'),
    url(r'^(?P<slug>[-\w]+)/locations.json$', views.testbed_locations_json,
        name='testbed_locations_json'),
]
