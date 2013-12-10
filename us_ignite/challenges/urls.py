from django.conf.urls import patterns, url


urlpatterns = patterns(
    'us_ignite.challenges.views',
    url(r'^$', 'challenge_list', name='challenge_list'),
)
