from django.conf.urls import patterns, url


def url_template(path, name=None):
    name = name if name else path
    template = '%s.html' % path
    return url(r'^%s/$' % path, 'render_template',
               {'template': template}, name=name)

urlpatterns = patterns(
    'us_ignite.get-involved.views',
    url(r'^$', 'render_template', {'template': 'about.html'}, name='about'),
    url_template('involve-developers'),
    url_template('involve-partners'),
    url_template('involve-communities'),
    url_template('involve-communities-learn'),
)
