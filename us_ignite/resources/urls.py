from django.conf.urls import patterns, url

urlpatterns = patterns(
    'us_ignite.resources.views',
    url(r'^$', 'resource_list', name='resource_list'),
    url(r'^(?P<slug>[-\w]+)/$', 'resource_detail', name='resource_detail'),
)
