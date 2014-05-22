from django.conf.urls import patterns, url

urlpatterns = patterns(
    'us_ignite.events.views',
    url(r'^$', 'event_list', name='event_list'),
    url(r'^past/$', 'event_list', {'timeframe': 'past'},
        name='event_list_past'),
    url(r'^add/$', 'event_add', name='event_add'),
    url(r'^(?P<slug>[-\w]+)/$', 'event_detail', name='event_detail'),
    url(r'^(?P<slug>[-\w]+)/edit/$', 'event_edit', name='event_edit'),
    url(r'^(?P<slug>[-\w]+)/ics/$', 'event_detail_ics',
        name='event_detail_ics'),
)
