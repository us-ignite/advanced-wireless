from django.conf.urls import patterns, url


urlpatterns = patterns(
    'us_ignite.actionclusters.views',
    url(r'^$', 'actioncluster_list', name='actioncluster_list'),
    #url(r'^apply/$', 'actioncluster_application', name='actioncluster_application'),
    url(r'^(?P<slug>[-\w]+)/$', 'actioncluster_detail', name='actioncluster_detail'),
    url(r'^(?P<slug>[-\w]+)/locations.json$', 'actioncluster_locations_json',
        name='actioncluster_locations_json'),
    url(r'^(?P<slug>[-\w]+)/membership/$', 'actioncluster_membership',
        name='actioncluster_membership'),
    url(r'^(?P<slug>[-\w]+)/edit/$', 'actioncluster_edit', name='actioncluster_edit'),
)
