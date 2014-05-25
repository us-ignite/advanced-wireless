from django.conf.urls import patterns, url

urlpatterns = patterns(
    'us_ignite.visualize.views',
    url(r'^$', 'visual_list', name='visual_list'),
    url(r'^data.json$', 'visual_json', name='visual_json'),
)
