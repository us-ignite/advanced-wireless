from django.conf.urls import patterns, url


urlpatterns = patterns(
    'us_ignite.organizations.views',
    url(r'^$', 'organization_list', name='organization_list'),
    url(r'^(?P<slug>[-\w]+)/$', 'organization_detail',
        name='organization_detail'),
    url(r'^(?P<slug>[-\w]+)/edit/$', 'organization_edit',
        name='organization_edit'),
)
