from django.conf.urls import patterns, url

urlpatterns = patterns(
    'us_ignite.resources.views',
    url(r'^(?P<slug>[-\w]+)/$', 'resource_detail', name='resource_detail'),
)
