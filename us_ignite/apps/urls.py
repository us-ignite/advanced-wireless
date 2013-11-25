from django.conf.urls import patterns, url


urlpatterns = patterns(
    'us_ignite.apps.views',
    url(r'^$', 'app_list', name='app_list'),
    url(r'^add/$', 'app_add', name='app_add'),
    url(r'^featured/$', 'apps_featured', name='apps_featured'),
    url(r'^featured/archive/(?P<slug>[-\w]+)/$', 'apps_featured_archive',
        name='apps_featured_archive'),
    url(r'^(?P<slug>[-\w]+)/$', 'app_detail', name='app_detail'),
    url(r'^(?P<slug>[-\w]+)/edit/$', 'app_edit', name='app_edit'),
    url(r'^(?P<slug>[-\w]+)/export/$', 'app_export', name='app_export'),
    url(r'^(?P<slug>[-\w]+)/version/$', 'app_version_add',
        name='app_version_add'),
    url(r'^(?P<slug>[-\w]+)/version/(?P<version_slug>[-\w]+)/$',
        'app_version_detail', name='app_version_detail'),
    url(r'^(?P<slug>[-\w]+)/membership/$', 'app_membership',
        name='app_membership'),
    url(r'^(?P<slug>[-\w]+)/membership/remove/(?P<membership_id>\d+)/$',
        'app_membership_remove', name='app_membership_remove'),
)
