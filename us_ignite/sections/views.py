from django.http import Http404
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404

from us_ignite.apps.models import Application
from us_ignite.hubs.models import Hub
from us_ignite.resources.models import Resource
from us_ignite.sections.models import SectionPage


def home(request):
    """Homepage of the application.

    List latest featured content.
    """
    context = {
        'application': Application.published.get_homepage(),
        'hub': Hub.active.get_homepage(),
        'resource': Resource.published.get_homepage(),
    }
    return TemplateResponse(request, 'home.html', context)


def render_template(request, template, prefix='sections'):
    context = {
        'prefix': prefix,
        'slug': template.replace('.html', '')
    }
    template = '%s/%s' % (prefix, template)
    return TemplateResponse(request, template, context)


def section_page_detail(request, section, slug, template='sections/base.html'):
    instance = get_object_or_404(SectionPage, slug=slug, section=section)
    if not instance.is_visible_by(request.user):
        raise Http404
    template = instance.template if instance.template else template
    context = {
        'object': instance,
        'title': instance.title,
        'slug': instance.slug,
        'body': instance.body,
    }
    return TemplateResponse(request, template, context)
