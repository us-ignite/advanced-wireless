from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

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
    }
    return TemplateResponse(request, 'events/object_detail.html', context)


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
