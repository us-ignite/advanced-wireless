from django.conf.urls import patterns, url


urlpatterns = patterns(
    'us_ignite.advanced_wireless_testbed.views',
    url(r'^$', 'awt_frontpage', name='awt_frontpage'),
)
