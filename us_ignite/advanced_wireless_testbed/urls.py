from django.conf.urls import patterns, url


urlpatterns = patterns(
    'us_ignite.advanced_wireless_testbed.views',
    url(r'^$', 'awt_frontpage', name='awt_frontpage'),
    url(r'^awt_default_subscribe/$', 'awt_default_subscribe', name='awt_default_subscribe'),
)
