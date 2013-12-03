from django.conf.urls import patterns, url

urlpatterns = patterns(
    'us_ignite.events.views',
    url(r'^(?P<slug>[-\w]+)/$', 'event_detail', name='event_detail'),
)
