from django.conf.urls import patterns, url

urlpatterns = patterns(
    'us_ignite.resources.views',
    url(r'^$', 'resource_list', name='resource_list'),
    url(r'^add/$', 'resource_add', name='resource_add'),
    url(r'^(?P<slug>[-\w]+)/$', 'resource_detail', name='resource_detail'),
    url(r'^(?P<slug>[-\w]+)/edit/$', 'resource_edit', name='resource_edit'),
)
