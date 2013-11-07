from django.conf.urls import patterns, url


urlpatterns = patterns(
    'us_ignite.apps.views',
    url(r'^$', 'app_list', name='app_list'),
)
