from django.conf.urls import patterns, url


urlpatterns = patterns(
    'us_ignite.hubs.views',
    url(r'^$', 'hub_list', name='hub_list'),
    url(r'^apply/$', 'hub_application', name='hub_application'),
    url(r'^(?P<slug>[-\w]+)/$', 'hub_detail', name='hub_detail'),
    url(r'^(?P<slug>[-\w]+)/membership/$', 'hub_membership',
        name='hub_membership'),
    url(r'^(?P<slug>[-\w]+)/edit/$', 'hub_edit', name='hub_edit'),
)
