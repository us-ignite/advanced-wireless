from django.conf.urls import patterns, url


urlpatterns = patterns(
    'us_ignite.apps.views',
    url(r'^$', 'app_list', name='app_list'),
    url(r'^add/$', 'app_add', name='app_add'),
    url(r'^(?P<slug>[-\w]+)/$', 'app_detail', name='app_detail'),
    url(r'^(?P<slug>[-\w]+)/edit/$', 'app_edit', name='app_edit'),
    url(r'^(?P<slug>[-\w]+)/membership/$', 'app_membership',
        name='app_membership'),
    url(r'^(?P<slug>[-\w]+)/membership/remove/(?P<membership_id>\d+)/$',
        'app_membership_remove', name='app_membership_remove'),
)
