from django.conf.urls import patterns, url


urlpatterns = patterns(
    'us_ignite.challenges.views',
    url(r'^$', 'challenge_list', name='challenge_list'),
    url(r'^(?P<slug>[-\w]+)/$', 'challenge_detail', name='challenge_detail'),
    url(r'^(?P<challenge_slug>[-\w]+)/enter/(?P<app_slug>[-\w]+)/$',
        'challenge_entry', name='challenge_entry'),
)
