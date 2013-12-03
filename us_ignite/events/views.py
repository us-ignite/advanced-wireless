from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from us_ignite.events.models import Event


def event_detail(request, slug):
    event = get_object_or_404(Event, slug__exact=slug)
    if not event.is_visible_by(request.user):
        raise Http404
    context = {
        'object': event,
        'hub_list': event.hubs.all(),
    }
    return TemplateResponse(request, 'events/object_detail.html', context)
