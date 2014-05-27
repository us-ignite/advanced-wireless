from django.conf.urls import patterns, url


urlpatterns = patterns(
    'us_ignite.testbeds.views',
    url(r'^$', 'testbed_list', name='testbed_list'),
    url(r'^(?P<slug>[-\w]+)/$', 'testbed_detail', name='testbed_detail'),
    url(r'^(?P<slug>[-\w]+)/locations.json$', 'testbed_locations_json',
        name='testbed_locations_json'),
)
