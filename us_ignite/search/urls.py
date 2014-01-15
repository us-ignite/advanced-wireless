from django.conf.urls import patterns, url


urlpatterns = patterns(
    'us_ignite.search.views',
    url(r'apps/', 'search_apps', name='search_apps'),
    url(r'events/', 'search_events', name='search_events'),
)
