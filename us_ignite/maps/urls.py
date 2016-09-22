from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.location_list, name='location_list'),
    url(r'^locations.json$', views.location_list_json, name='location_list_json'),
]
