from django.conf.urls import patterns, url
from django.views.generic import TemplateView


to_template = lambda t: TemplateView.as_view(template_name=t)

urlpatterns = patterns(
    'us_ignite.globalcityteams.views',
    url(r'^$', to_template('globalcityteams/index.html'), name='globalcityteams'),
    url(r'^faq/$', to_template('globalcityteams/faq.html'), name='globalcityteams_faq'),
    url(r'^partners/$', to_template('globalcityteams/partners.html'), name='globalcityteams_partners'),
    url(r'^sectors/$', to_template('globalcityteams/sectors.html'), name='globalcityteams_sectors'),
    url(r'^about/$', to_template('globalcityteams/about.html'), name='globalcityteams_about'),
    url(r'^looking-for-partners/$', to_template('globalcityteams/looking_for_partners.html'), name='globalcityteams_looking_for_partners'),
    url(r'^upload/$', to_template('globalcityteams/document-upload.html')),
    url(r'^events/$', 'event_list', name='event_list'),
    url(r'^news/$', 'article_list', name='article_list'),
    url(r'^search/$', 'search', name='search'),

)
