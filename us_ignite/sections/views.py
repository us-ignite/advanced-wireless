from django.template.response import TemplateResponse

from us_ignite.apps.models import Application
from us_ignite.hubs.models import Hub
from us_ignite.resources.models import Resource


def home(request):
    """Homepage of the application.

    List latest featured content.
    """
    context = {
        'application': Application.published.get_featured(),
        'hub': Hub.active.get_featured(),
        'resource': Resource.published.get_featured(),
    }
    return TemplateResponse(request, 'home.html', context)


def render_template(request, template):
    context = {}
    template = 'sections/%s' % template
    return TemplateResponse(request, template, context)
