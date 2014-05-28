from django.conf.urls import patterns, url

urlpatterns = patterns(
    'us_ignite.people.views',
    url(r'^$', 'profile_list', name='profile_list'),
    url(r'^(?P<slug>[-_\w]{1,32})/$', 'profile_detail', name='profile_detail'),
)
