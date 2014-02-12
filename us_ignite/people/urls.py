from django.conf.urls import patterns, url

urlpatterns = patterns(
    'us_ignite.people.views',
    url(r'^(?P<slug>[-\w]{1,32})/$', 'profile_detail', name='profile_detail'),
)
