from django.conf.urls import url
from . import views


urlpatterns = [
    url(r'^$', views.post_list, name='blog_post_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>[-\w]+)/$',
        views.post_detail, name='blog_post_detail'),
]
