from django.conf.urls import patterns, url


urlpatterns = patterns(
    'us_ignite.advanced_wireless_testbed.views',
    url(r'^$', 'awt_frontpage', name='awt_frontpage'),
    url(r'^awt_default_subscribe/potential_proposer/$', 'awt_potential_proposer', {'form': 'potential_proposer'}, name='awt_potential_proposer'),
    url(r'^awt_default_subscribe/companies/$', 'awt_companies', {'form': 'companies'},name='awt_companies'),
    url(r'^awt_default_subscribe/interested_observers/$', 'awt_interested_observers', {'form': 'interested_observers'}, name='awt_interested_observers'),
)
