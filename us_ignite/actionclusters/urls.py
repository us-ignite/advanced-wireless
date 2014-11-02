from django.conf.urls import patterns, url


urlpatterns = patterns(
    'us_ignite.actionclusters.views',
    url(r'^$', 'actioncluster_list', name='actioncluster_list'),
    url(r'^add/$', 'actioncluster_add', name='actioncluster_add'),
    url(r'^featured/$', 'actionclusters_featured',
        name='actionclusters_featured'),
    url(r'^featured/archive/(?P<slug>[-\w]+)/$',
        'actionclusters_featured_archive',
        name='actionclusters_featured_archive'),
    url(r'^(?P<slug>[-\w]+)/$', 'actioncluster_detail',
        name='actioncluster_detail'),
    url(r'^(?P<slug>[-\w]+)/edit/$', 'actioncluster_edit',
        name='actioncluster_edit'),
    url(r'^(?P<slug>[-\w]+)/export/$', 'actioncluster_export',
        name='actioncluster_export'),
    url(r'^(?P<slug>[-\w]+)/hubs-membership/$', 'actioncluster_hub_membership',
        name='actioncluster_hub_membership'),
    url(r'^(?P<slug>[-\w]+)/membership/$', 'actioncluster_membership',
        name='actioncluster_membership'),
    url(r'^domain/(?P<domain>[-\w]+)/$', 'actioncluster_list',
        name='actioncluster_list_domain'),
    url(r'^stage/(?P<stage>[\d]{1})/$', 'actioncluster_list',
        name='actioncluster_list_stage'),
)
