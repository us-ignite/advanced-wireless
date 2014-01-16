from django.conf.urls import patterns, url


urlpatterns = patterns(
    'us_ignite.search.views',
    url(r'apps/', 'search_apps', name='search_apps'),
    url(r'events/', 'search_events', name='search_events'),
    url(r'hubs/', 'search_hubs', name='search_hubs'),
    url(r'orgs/', 'search_organizations', name='search_organizations'),
)
