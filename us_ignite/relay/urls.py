from django.conf.urls import patterns, url


urlpatterns = patterns(
    'us_ignite.relay.views',
    url(r'^(?P<slug>[-\w]+)/$', 'contact_user', name='contact_user'),
)
