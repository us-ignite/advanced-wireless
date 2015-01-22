from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from django.views.generic import RedirectView


to_template = lambda t: TemplateView.as_view(template_name=t)

urlpatterns = patterns(
    'us_ignite.globalcityteams.views',
    url(r'^$', to_template('globalcityteams/index.html'),
        name='globalcityteams'),
    url(r'^faq/$', to_template('globalcityteams/faq.html'),
        name='globalcityteams_faq'),
    url(r'^partners/$', to_template('globalcityteams/partners.html'),
        name='globalcityteams_partners'),
    url(r'^sectors/$', to_template('globalcityteams/sectors.html'),
        name='globalcityteams_sectors'),
    url(r'^about/$', to_template('globalcityteams/about.html'),
        name='globalcityteams_about'),
    url(r'^upload/$', to_template('globalcityteams/document-upload.html')),
    url(r'^events/$', 'event_list', name='event_list'),
    url(r'^events/(?P<slug>[-\w]+)/$', 'event_detail', name='event_detail'),
    url(r'^search/$', 'search', name='search'),
    url(r'^news/$', 'post_list', name='news_list'),
    url(r'^news/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>[-\w]+)/$',
        'post_detail', name='news_detail'),
    url(r'^subscribe/$', 'mailing_subscribe', name='subscribe'),
    url(r'^TechJam2015?/$', RedirectView.as_view(
        url='https://s3.amazonaws.com/us-ignite-org/static/pdf/20150120+Global+City+Teams+TECH+JAM+Prelim+Agenda+V5+Short+SR.pdf'), 
        name='tech_jam_2015_pdf'),
)
