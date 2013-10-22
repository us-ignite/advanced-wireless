from django.conf.urls import patterns, url

urlpatterns = patterns(
    'us_ignite.people.views',
    url(r'^$', 'people_list', name='people_list'),
)
