from django.conf.urls import url
from . import views


def url_template(path, name=None):
    name = name if name else path
    template = '%s.html' % path
    return url(r'^%s/$' % path, views.render_template,
               {'template': template}, name=name)

urlpatterns = [
    # 'us_ignite.sections.views',
    url(r'^$', views.render_template, {'template': 'about.html'}, name='about'),
    url_template('what-is-us-ignite'),
    url_template('mission'),
    url_template('technologies'),
    url_template('contact-us'),
    url_template('staff'),
    url_template('board-of-directors'),
    url_template('faq'),
    url_template('partners'),
    url_template('what-we-do'),
]
