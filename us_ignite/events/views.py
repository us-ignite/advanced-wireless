from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils import timezone

from icalendar import Calendar, Event as CalEvent
from us_ignite.common import pagination
from us_ignite.events.forms import EventForm
from us_ignite.events.models import Event


def event_detail(request, slug):
    """Detail of an ``Event``."""
    event = get_object_or_404(Event, slug__exact=slug)
    if not event.is_visible_by(request.user):
        raise Http404
    context = {
        'object': event,
        'hub_list': event.hubs.all(),
        'is_owner': event.is_owner(request.user),
    }
    return TemplateResponse(request, 'events/object_detail.html', context)


def event_detail_ics(request, slug):
    event_obj = get_object_or_404(Event.published, slug__exact=slug)
    calendar = Calendar()
    calendar.add('prodid', '-//US Ignite//us-ignite.org//')
    calendar.add('version', '1.0')
    event = CalEvent()
    event.add('summary', event_obj.name)
    event.add('dtstart', event_obj.start_datetime)
    if event_obj.end_datetime:
        event.add('dtend', event_obj.end_datetime)
    event.add('dtstamp', timezone.now())
    event['uid'] = '%s/%s@us-ignite.org' % (event_obj.pk, timezone.now())
    event.add('priority', 5)
    calendar.add_component(event)
    response = HttpResponse(calendar.to_ical(), content_type='text/calendar')
    response['Content-Disposition'] = 'attachment; filename="event.ics"'
    return response


@login_required
def event_add(request):
    """Form to add an ``Event``. Only authenticated users can add events."""
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            form.save_m2m()
            messages.success(
                request, 'The event "%s" has been added.' % instance.name)
            return redirect(instance.get_absolute_url())
    else:
        form = EventForm()
    context = {
        'form': form,
    }
    return TemplateResponse(request, 'events/object_add.html', context)


@login_required
def event_edit(request, slug):
    event = get_object_or_404(
        Event.published, slug__exact=slug, user=request.user)
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        if form.is_valid():
            instance = form.save()
            messages.success(
                request, 'The event "%s" has been updated.' % instance.name)
            return redirect(instance.get_absolute_url())
    else:
        form = EventForm(instance=event)
    context = {
        'object': event,
        'form': form,
    }
    return TemplateResponse(request, 'events/object_edit.html', context)


def event_list(request):
    page_no = pagination.get_page_no(request.GET)
    now = timezone.now()
    object_list = Event.published.filter(start_datetime__gte=now)
    page = pagination.get_page(object_list, page_no)
    context = {
        'page': page,
    }
    return TemplateResponse(request, 'events/object_list.html', context)
