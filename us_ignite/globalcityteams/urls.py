from django.conf.urls import patterns, url
from django.views.generic import TemplateView


to_template = lambda t: TemplateView.as_view(template_name=t)

urlpatterns = patterns(
    '',
    url(r'^$', to_template('globalcityteams/index.html')),
    url(r'^faq/$', to_template('globalcityteams/faqs.html')),
    url(r'^about/$', to_template('globalcityteams/about.html')),
    url(r'^upload/$', to_template('globalcityteams/document-upload.html')),
)
