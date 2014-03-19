from django.conf.urls import patterns, url


def url_template(path, name=None):
    name = name if name else path
    context = {
        'template': '%s.html' % path,
        'prefix': 'get-involved',
    }
    return url(r'^%s/$' % path, 'render_template', context, name=name)

urlpatterns = patterns(
    'us_ignite.sections.views',
    url_template('involve-developers'),
    url_template('involve-partners'),
    url_template('involve-communities'),
    url_template('involve-communities-learn'),
)
