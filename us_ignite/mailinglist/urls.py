from django.conf.urls import patterns, url

urlpatterns = patterns(
    'us_ignite.mailinglist.views',
    url(r'^$', 'mailing_subscribe', name='mailing_subscribe'),
)
