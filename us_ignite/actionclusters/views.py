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
from us_ignite.actionclusters.models import ActionCluster
#from us_ignite.hubs import forms, mailer
from us_ignite.maps.utils import get_location_dict


@login_required

def actioncluster_list(request):
    """List al the available ``Hubs``."""
    page_no = pagination.get_page_no(request.GET)
    object_list = ActionCluster.active.all()
    page = pagination.get_page(object_list, page_no)
    featured_list = ActionCluster.active.filter(is_featured=True)[:3]
    context = {
        'page': page,
        'featured_list': featured_list,
    }
    return TemplateResponse(request, 'hubs/object_list.html', context)


def actioncluster_detail(request, slug):
    """Homepage of a Ignite Community.

    This view aggregates all the content related to this ``Hub``. Available
    when published or to the ``contact``.
    """
    instance = get_object_or_404(
        ActionCluster.objects.select_related('contact'), slug__exact=slug)
    if not instance.is_visible_by(request.user):
        raise Http404
    membership_list = instance.actionclustermembership_set.select_related('profile').all()
    member_list = [m.user for m in membership_list]
    # Determine if the user is a member of this ``Hub``:
    is_member = request.user in member_list
    activity_list = (instance.actionclusteractivity_set
                     .select_related('user').all()[:20])
    #event_list = Event.published.get_upcoming(hubs=instance)[:5]
    #actioncluster_award_list = (instance.hubaward_set
    #                  .select_related('award').all())
    #award_list = [ha.award for ha in actioncluster_award_list]
    #testbed_list = instance.testbed_set.all()
    context = {
        'object': instance,
        'feature_list': instance.features.all(),
        'member_list': member_list,
        'is_member': is_member,
        'is_contact': instance.is_contact(request.user),
        'activity_list': activity_list,
     #   'event_list': event_list,
     #   'award_list': award_list,
     #   'testbed_list': testbed_list,
    }
    return TemplateResponse(request, 'actionclusters/object_detail.html', context)

@require_http_methods(['POST'])
@login_required
def actioncluster_membership(request, slug):
    """Associates the user with the selected community"""
    instance = get_object_or_404(
        ActionCluster.objects, slug__exact=slug, status=ActionCluster.PUBLISHED)
    ActionClusterMembership.objects.get_or_create(user=request.user, actioncluster=instance)
    messages.success(request, 'You are now part of %s.' % instance.name)
    return redirect(instance.get_absolute_url())

@login_required
def actioncluster_edit(request, slug):
    """Allows ``contacts`` to edit a ``Hub``. """
    instance = get_object_or_404(
        ActionCluster.objects, slug__exact=slug, contact=request.user)
    if request.method == 'POST':
        form = forms.HubForm(request.POST, request.FILES, instance=instance)
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


def actioncluster_locations_json(request, slug):
    hub = get_object_or_404(ActionCluster.active, slug__exact=slug)
    raw_user_list = get_users(hub)
    # Get events with location
    item_list = get_event_list(hub)
    hub_dict = get_location_dict(hub, 'community')
    if hub_dict:
        item_list += [hub_dict]
    item_list += get_user_list(raw_user_list)
    item_list += get_organization_list(raw_user_list)
    item_list += get_app_member_list(hub)
    return json_response(item_list, callback='map.render')

def get_users(hub):
    queryset = hub.actionclustermembership_set.select_related('user__profile').all()
    return [h.user for h in queryset]

def get_user_list(user_list):
    new_user_list = []
    for user in user_list:
        profile = user.get_profile()
        if profile:
            new_user_list.append(get_location_dict(profile, 'user'))
    return new_user_list


def get_organization_list(user_list):
    new_org_list = []
    for user in user_list:
        org_list = (user.organizationmember_set
                    .select_related('organization').all().distinct())
        for membership in org_list:
            org = membership.organization
            new_org_list.append(get_location_dict(org, 'organization'))
    return new_org_list


def get_app_member_list(hub):
    hub_queryset = (hub.actionclustermembership_set
                    .select_related('application').all())
    apps_member_list = []
    for membership in hub_queryset:
        app = membership.application
        apps_member_list.append(get_location_dict(app, 'app-member'))
    return apps_member_list

def get_event_list(hub):
    event_list = []
    for event in Event.published.get_upcoming(hubs=hub):
        if event.position.longitude and event.position.latitude:
            event_list.append(get_location_dict(event, 'event'))
    return event_list