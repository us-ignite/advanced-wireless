from django.conf.urls import url
from . import views
from django.views.generic import TemplateView
from django.views.generic import RedirectView


to_template = lambda t: TemplateView.as_view(template_name=t)

urlpatterns = [
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

    url(r'^leadership-fund/$', to_template('globalcityteams/leadership_fund.html'), name='globalcityteams_leadership_fund'),
    url(r'^leadership-fund/travel-application/$', to_template('globalcityteams/leadership_fund_travel_application.html'), name='globalcityteams_leadership_fund_travel_application'),
    url(r'^leadership-fund/leadership-application/$', to_template('globalcityteams/leadership_fund_leadership_application.html'), name='globalcityteams_leadership_fund_leadership_application'),

    url(r'^upload/$', to_template('globalcityteams/document-upload.html')),
    url(r'^events/$', views.event_list, name='event_list'),
    url(r'^events/(?P<slug>[-\w]+)/$', views.event_detail, name='event_detail'),
    url(r'^search/$', views.search, name='search'),
    # url(r'^news/$', views.post_list, name='news_list'),
    # url(r'^news/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>[-\w]+)/$',
    #     views.post_detail, name='news_detail'),
    url(r'^subscribe/$', views.mailing_subscribe, name='subscribe'),
    url(r'^TechJam2015?/$', RedirectView.as_view(
        url='https://s3.amazonaws.com/us-ignite-org/static/pdf/Global+City+Teams+TECH+JAM+Prelim+Agenda.pdf'), name='tech_jam_2015_pdf'),
]
