from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods

from us_ignite.common import pagination
from us_ignite.common.response import json_response
from us_ignite.events.models import Event
from us_ignite.hubs.models import Hub, HubRequest, HubMembership
from us_ignite.hubs import forms, mailer


@login_required
def hub_application(request):
    """View to submit a ``Hub`` for consideration"""
    object_list = HubRequest.objects.filter(
        ~Q(status=HubRequest.REMOVED), user=request.user)
    if request.method == 'POST':
        form = forms.HubRequestForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            # Notify US Ignite about this request:
            mailer.notify_request(instance)
            msg = 'Your application "%s" has been sent.' % instance.name
            messages.success(request, msg)
            return redirect('home')
    else:
        form = forms.HubRequestForm()
    context = {
        'form': form,
        'object_list': object_list,
    }
    return TemplateResponse(request, 'hubs/object_application.html', context)


def hub_detail(request, slug):
    """Homepage of a Ignite Community.

    This view aggregates all the content related to this ``Hub``. Available
    when published or to the ``contact``.
    """
    instance = get_object_or_404(
        Hub.objects.select_related('contact'), slug__exact=slug)
    if not instance.is_visible_by(request.user):
        raise Http404
    membership_list = instance.hubmembership_set.select_related('profile').all()
    member_list = [m.user for m in membership_list]
    # Determine if the user is a member of this ``Hub``:
    is_member = request.user in member_list
    activity_list = (instance.hubactivity_set
                     .select_related('user').all()[:20])
    event_list = Event.published.get_upcoming(hubs=instance)[:5]
    hub_award_list = (instance.hubaward_set
                      .select_related('award').all())
    award_list = [ha.award for ha in hub_award_list]
    context = {
        'object': instance,
        'feature_list': instance.features.all(),
        'member_list': member_list,
        'is_member': is_member,
        'is_contact': instance.is_contact(request.user),
        'activity_list': activity_list,
        'event_list': event_list,
        'award_list': award_list,
    }
    return TemplateResponse(request, 'hubs/object_detail.html', context)


@require_http_methods(['POST'])
@login_required
def hub_membership(request, slug):
    """Associates the user with the selected community"""
    instance = get_object_or_404(
        Hub.objects, slug__exact=slug, status=Hub.PUBLISHED)
    HubMembership.objects.get_or_create(user=request.user, hub=instance)
    messages.success(request, 'You are now part of %s.' % instance.name)
    return redirect(instance.get_absolute_url())


@login_required
def hub_edit(request, slug):
    """Allows ``contacts`` to edit a ``Hub``. """
    instance = get_object_or_404(
        Hub.objects, slug__exact=slug, contact=request.user)
    if request.method == 'POST':
        form = forms.HubForm(request.POST, instance=instance)
        if form.is_valid():
            instance = form.save()
            msg = '%s has been updated successfully' % instance.name
            messages.success(request, msg)
            return redirect(instance.get_absolute_url())
    else:
        form = forms.HubForm(instance=instance)
    context = {
        'form': form,
        'object': instance,
    }
    return TemplateResponse(request, 'hubs/object_edit.html', context)


def hub_list(request):
    """List al the available ``Hubs``."""
    page_no = pagination.get_page_no(request.GET)
    object_list = Hub.active.all()
    page = pagination.get_page(object_list, page_no)
    context = {
        'page': page,
    }
    return TemplateResponse(request, 'hubs/object_list.html', context)


def get_event_list(hub):
    event_list = []
    for event in Event.published.get_upcoming(hubs=hub):
        if event.position.longitude and event.position.latitude:
            event_list.append(event.get_location_dict())
    return event_list


def hub_locations_json(request, slug):
    hub = get_object_or_404(Hub.active, slug__exact=slug)
    # Get events with location
    event_list = get_event_list(hub)
    return json_response(event_list, callback='map.render')
