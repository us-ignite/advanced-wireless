from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from django.contrib import admin

admin.autodiscover()

# custom 404 and 500 handlers
handler404 = 'us_ignite.common.views.custom_404'
handler500 = 'us_ignite.common.views.custom_500'

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('us_ignite.profiles.urls')),
    url(r'^people/', include('us_ignite.people.urls')),
    url(r'^apps/', include('us_ignite.apps.urls')),
    url(r'^hub/', include('us_ignite.hubs.urls')),
    url(r'^event/', include('us_ignite.events.urls')),
    url(r'^org/', include('us_ignite.organizations.urls')),
    url(r'^challenges/', include('us_ignite.challenges.urls')),
    url(r'^contact/', include('us_ignite.relay.urls')),
    url(r'^resources/', include('us_ignite.resources.urls')),
    url(r'^blog/', include('us_ignite.blog.urls')),
    url(r'^search/', include('us_ignite.search.urls')),
    url(r'^map/', include('us_ignite.maps.urls')),
    url(r'^browserid/', include('django_browserid.urls')),
)

urlpatterns += patterns(
    'us_ignite.common.views',
    url(r'^404/$', 'custom_404', name='http404'),
    url(r'^500/$', 'custom_500', name='http500'),
)

# Static templates:
urlpatterns += patterns(
    '',
    url(r'^robots.txt$', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),
)

# US Ignite legacy redirects:
urlpatterns += patterns(
    '',
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>[-\w]+)/$',
        'us_ignite.blog.views.legacy_redirect', name='legacy_post'),
)

if settings.DEBUG:
    urlpatterns += patterns(
        '',
        url(r'^screens/$', TemplateView.as_view(template_name='screens.html')),
    )

    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += patterns(
        '',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )
