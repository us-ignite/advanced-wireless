from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from django.views.generic import RedirectView

from django.contrib import admin

admin.autodiscover()


# custom 404 and 500 handlers
handler404 = 'us_ignite.common.views.custom_404'
handler500 = 'us_ignite.common.views.custom_500'

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns(
    'us_ignite.advanced_wireless_testbed.views',
    url(r'^$', 'awt_frontpage', name='awt_frontpage'),

    url(r'^rfp/$', RedirectView.as_view(url='https://www.advancedwireless.org#sec_nine')),

    url(r'^awt_default_subscribe/potential_proposers/$', 'awt_default_subscribe', {'form': 'potential_proposers'},
        name='awt_potential_proposers'),
    url(r'^awt_default_subscribe/companies/$', 'awt_default_subscribe', {'form': 'companies'}, name='awt_companies'),
    url(r'^awt_default_subscribe/interested_observers/$', 'awt_default_subscribe', {'form': 'interested_observers'},
        name='awt_interested_observers'),
    url(r'^awt_default_subscribe/$', 'awt_default_subscribe', name='awt_default_subscribe'),
    # url(r'^dashboard/$', 'us_ignite.people.views.dashboard', name='dashboard'),
    # url(r'^accounts/', include('us_ignite.profiles.urls')),
    # url(r'^people/', include('us_ignite.people.urls')),
    # url(r'^apps/', include('us_ignite.apps.urls')),
    # url(r'^hub/', include('us_ignite.hubs.urls')),
    # url(r'^testbed/', include('us_ignite.testbeds.urls')),
    # url(r'^event/', include('us_ignite.events.urls')),
    # url(r'^org/', include('us_ignite.organizations.urls')),
    # url(r'^challenges/', include('us_ignite.challenges.urls')),
    # url(r'^contact/', include('us_ignite.relay.urls')),
    # url(r'^resources/', include('us_ignite.resources.urls')),
    # url(r'^blog/', include('us_ignite.blog.urls')),
    # url(r'^search/', include('us_ignite.search.urls')),
    # url(r'^map/', include('us_ignite.maps.urls')),
    # url(r'^news/', include('us_ignite.news.urls')),
    # url(r'^subscribe/', include('us_ignite.mailinglist.urls')),
    # url(r'^overview/', include('us_ignite.visualize.urls')),
    # url(r'^browserid/', include('django_browserid.urls')),
    # url(r'^smart-gigabit-communities/', include('us_ignite.smart_gigabit_communities.urls')),
    # url(r'^sgcreversepitch/', RedirectView.as_view(pattern_name='smart_gigabit_communities_reverse_pitch')),
)
#
# # Global city teams:
# urlpatterns += patterns(
#     '',
#     url(r'^globalcityteams/actioncluster/',
#         include('us_ignite.actionclusters.urls')),
#     url(r'^globalcityteams/',
#         include('us_ignite.globalcityteams.urls', namespace='globalcityteams')),
#     url(r'^globalcityteams/participation-guide', TemplateView.as_view(template_name='globalcityteams/participation-guide.html'))
# )
#
#
# urlpatterns += patterns(
#     '',
#     url(r'^about/', include('us_ignite.sections.urls')),
#     url(r'^get-involved/', include('us_ignite.sections.urls_get_involved')),
#     url(r'^get-involved/(?P<slug>(welcome|identify-a-community-leader-cl|identify-a-technical-leader-tl|creation-of-community-profile|start-identifying-local-partnerships-and-engaging|start-to-identify-potential-gigabit-applications|on-going-activities|sgc-resources))/', 'us_ignite.sections.views.section_page_gigabit', name='section_gigabit'),
#     url(r'^(?P<section>(about|get-involved))/(?P<slug>[-\w]+)/$',
#         'us_ignite.sections.views.section_page_detail',
#         name='section_page_detail'),
# )

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
    # url(r'^kit/$', TemplateView.as_view(template_name='kit.html')),
    # url(r'^march2015/$', RedirectView.as_view(url='/smartfuture2015')),
    # url(r'^smartfuture2015/$', TemplateView.as_view(template_name='march2015_2.html')),
    # url(r'^(?i)gctcexpo/$', TemplateView.as_view(template_name='gctc-expo2016.html')),
    # url(r'^(?i)gctcexpowebcast/$', TemplateView.as_view(template_name='gctc-expo_webcast.html')),
    # url(r'^(?i)globalcityteamsfestival?/$', RedirectView.as_view(url='http://us-ignite.org/globalcityteamsexpo'), name='global-city-teams-expo'),
    # url(r'^(?i)GCTCstrategyworkshop/$', TemplateView.as_view(template_name='gctc-strategy-workshop.html')),
    # url(r'^(?i)GCTC2016Kickoff/$', TemplateView.as_view(template_name='gctc-2016-kickoff.html')),
    # url(r'^(?i)smartcommunityweek/$', TemplateView.as_view(template_name='smartcommunityweek2016.html')),
    # url(r'^(?i)smartcommunityweekstudent/$', TemplateView.as_view(template_name='smartcommunityweekstudent.html')),
    # url(r'^(?i)smartcityworks/$', TemplateView.as_view(template_name='smartcityworks.html')),
    # url(r'^wireless/', include('us_ignite.advanced_wireless_testbed.urls')),

)


# US Ignite legacy redirects:
urlpatterns += patterns(
    '',
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>[-\w]+)/$',
        'us_ignite.blog.views.legacy_redirect', name='legacy_post'),
)

urlpatterns += patterns(
    '',
    url(r'^tiny_mce/(?P<path>.*)$', 'django.views.static.serve', {'document_root': 'us_ignite/assets/js/tiny_mce/'})
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

    # Used by the debug toolbar when DEBUG is on:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )
