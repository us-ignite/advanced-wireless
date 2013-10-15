from django.conf.urls import patterns, include, url


urlpatterns = patterns(
    'us_ignite.profiles.views',
    url(r'^register/$', 'registration_view', name='registration_register'),
    url(r'', include('registration.backends.default.urls')),
)
