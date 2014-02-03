from django.conf.urls import patterns, url


urlpatterns = patterns(
    'us_ignite.maps.views',
    url(r'^$', 'location_list', name='location_list'),
    url(r'^locations.json$', 'location_list_json', name='location_list_json'),
)
