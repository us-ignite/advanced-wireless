import pytz

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils import timezone

from icalendar import Calendar, vText, Event as CalEvent
from us_ignite.common import pagination
from us_ignite.events.forms import EventForm, EventURLFormSet
from us_ignite.events.models import Event


def event_detail(request, slug, section=Event.DEFAULT):
    """Detail of an ``Event``."""
    event = get_object_or_404(Event, slug__exact=slug, section=section)
    if not event.is_visible_by(request.user):
        raise Http404
    audience_list = [a for a in event.audiences.all()]
    audience_list += [event.audience_other]
    context = {
        'object': event,
        'hub_list': event.hubs.all(),
        'is_owner': event.is_owner(request.user),
        'audience_list': audience_list,
        'url_list': event.eventurl_set.all(),
    }
    return TemplateResponse(request, 'events/object_detail.html', context)


def _swap_timezone(timezone_name):
    TIMEZONE_EQUIVALENT = {
        'US/Eastern': 'America/New_York',
    }
    if timezone_name in TIMEZONE_EQUIVALENT:
        return TIMEZONE_EQUIVALENT[timezone_name]
    return timezone_name


def event_detail_ics(request, slug):
    event_obj = get_object_or_404(Event.published, slug__exact=slug)
    calendar = Calendar()
    calendar.add('prodid', '-//US Ignite//us-ignite.org//')
    calendar.add('version', '2.0')
    event = CalEvent()
    event.add('summary', event_obj.name)
    url = '%s%s' % (settings.SITE_URL, event_obj.get_absolute_url())
    description = event_obj.description + '\n\n' + url
    event.add('description', description)
    event.add('url', url)
    event['location'] = vText(event_obj.address)
    # Use timezone aware datetime objects:
    event_tz = pytz.timezone(_swap_timezone(event_obj.timezone))
    event.add('dtstart', event_obj.start_datetime.astimezone(event_tz))
    if event_obj.end_datetime:
        event.add('dtend', event_obj.end_datetime.astimezone(event_tz))
    event.add('dtstamp', timezone.now())
    event['uid'] = 'event-%s/@us-ignite.org' % (event_obj.pk)
    event.add('priority', 5)
    calendar.add_component(event)
    file_name = 'event-%s.ics' % event_obj.slug
    response = HttpResponse(calendar.to_ical(), content_type='text/calendar')
    response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
    return response


@login_required
def event_add(request):
    """Form to add an ``Event``. Only authenticated users can add events."""
    if request.method == 'POST':
        form = EventForm(request.POST)
        formset = EventURLFormSet(request.POST)
        if form.is_valid() and formset.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            form.save_m2m()
            # Save URL inline form:
            formset.instance = instance
            formset.save()
            messages.success(
                request, 'The event "%s" has been added.' % instance.name)
            return redirect(instance.get_absolute_url())
    else:
        form = EventForm()
        formset = EventURLFormSet()
    context = {
        'form': form,
        'formset': formset,
    }
    return TemplateResponse(request, 'events/object_add.html', context)


@login_required
def event_edit(request, slug):
    event = get_object_or_404(
        Event.objects, slug__exact=slug, user=request.user)
    if not event.is_visible_by(request.user):
        raise Http404
    if request.method == 'POST':
        form = EventForm(request.POST, instance=event)
        formset = EventURLFormSet(request.POST, instance=event)
        if form.is_valid() and formset.is_valid():
            instance = form.save()
            formset.save()
            messages.success(
                request, 'The event "%s" has been updated.' % instance.name)
            return redirect(instance.get_absolute_url())
    else:
        # Activate the current event timezone:
        timezone.activate(pytz.timezone(event.timezone))
        form = EventForm(instance=event)
        formset = EventURLFormSet(instance=event)
    context = {
        'object': event,
        'form': form,
        'formset': formset,
    }
    return TemplateResponse(request, 'events/object_edit.html', context)


def event_list(request, timeframe='upcoming', section=Event.DEFAULT):
    page_no = pagination.get_page_no(request.GET)
    now = timezone.now()
    TIMEFRAMES = {
        'upcoming': {'start_datetime__gte': now},
        'past': {'start_datetime__lte': now},
    }
    if not timeframe in TIMEFRAMES:
        raise Http404('Unexisting timeframe')
    object_list = Event.published.filter(
        section=section, **TIMEFRAMES[timeframe])
    page = pagination.get_page(object_list, page_no)
    featured_list = (Event.published
                     .filter(is_featured=True, **TIMEFRAMES['upcoming']))
    context = {
        'page': page,
        'timeframe': timeframe,
        'featured_list': featured_list,
    }
    return TemplateResponse(request, 'events/object_list.html', context)
