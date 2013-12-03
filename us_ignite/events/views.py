from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from us_ignite.events.models import Event


def event_detail(request, slug):
    event = get_object_or_404(Event.published, slug__exact=slug)
    context = {
        'object': event,
    }
    return TemplateResponse(request, 'events/object_detail.html', context)
