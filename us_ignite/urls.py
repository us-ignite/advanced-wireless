from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^accounts/', include('us_ignite.profiles.urls')),
    url(r'^people/', include('us_ignite.people.urls')),
    url(r'^browserid/', include('django_browserid.urls')),
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
