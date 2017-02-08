from django.conf.urls import patterns, url

urlpatterns = patterns(
    'us_ignite.smart_gigabit_communities.views',
    url(r'^reverse-pitch/$', 'reverse_pitch', name='smart_gigabit_communities_reverse_pitch'),
)
