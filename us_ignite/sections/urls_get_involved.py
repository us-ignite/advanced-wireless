from django.conf.urls import url
from . import views


def url_template(path, name=None):
    name = name if name else path
    context = {
        'template': '%s.html' % path,
        'prefix': 'get-involved',
    }
    return url(r'^%s/$' % path, views.render_template, context, name=name)

urlpatterns = [
    url_template('involve-developers'),
    url_template('involve-developers-learn'),
    url_template('involve-partners'),
    url_template('involve-communities'),
    url_template('involve-communities-learn'),
]
