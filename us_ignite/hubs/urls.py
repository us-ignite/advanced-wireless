from django.conf.urls import patterns, url


urlpatterns = patterns(
    'us_ignite.hubs.views',
    url(r'^apply/$', 'hub_application', name='hub_application'),
)
