from django.conf.urls import patterns, url


urlpatterns = patterns(
    'us_ignite.organizations.views',
    url(r'^(?P<slug>[-\w]+)/', 'organization_detail', name='organization_detail'),
)
