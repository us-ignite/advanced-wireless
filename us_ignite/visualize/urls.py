from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.visual_list, name='visual_list'),
    url(r'^data.json$', views.visual_json, name='visual_json'),
]
