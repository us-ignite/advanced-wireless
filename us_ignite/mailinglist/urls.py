from django.conf.urls import patterns, url

urlpatterns = patterns(
    'us_ignite.mailinglist.views',
    url(r'^$', 'mailing_subscribe', name='mailing_subscribe'),
    url(r'^(?P<slug>[-\w]+)/$', 'mailing_subscribe', name='mailing_subscribe'),
)
