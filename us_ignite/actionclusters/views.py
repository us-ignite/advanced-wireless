from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.loader import render_to_string
from django.template.response import TemplateResponse
from django.utils import timezone

from us_ignite.actionclusters import mailer
from us_ignite.actionclusters.forms import (
    ActionClusterForm,
    ActionClusterLinkFormSet,
    MembershipForm,
    ActionClusterMediaFormSet,
    ActionClusterMembershipFormSet
)
from us_ignite.actionclusters.models import (
    ActionCluster,
    ActionClusterMembership,
    Domain,
    Year
)
from us_ignite.awards.models import ActionClusterAward
from us_ignite.common import pagination
from us_ignite.hubs.forms import HubActionClusterMembershipForm
from us_ignite.hubs.models import HubActionClusterMembership


def get_stage_or_404(stage):
    for pk, name in ActionCluster.STAGE_CHOICES:
        if pk == int(stage):
            return (pk, name)
    raise Http404('Invalid stage.')


def actioncluster_list(request, current=True, domain=None, stage=None, year=None, filter_name='', description=''):
    """List all the available ``ActionCluster``."""
    extra_qs = {
        'is_approved': True,
        'status': ActionCluster.PUBLISHED,
    }
    if domain:
        # Validate domain is valid if provided:
        extra_qs['domain'] = get_object_or_404(Domain, slug=domain)
        filter_name = extra_qs['domain'].name
    elif stage:
        # Validate stage is valid if provided:
        pk, name = get_stage_or_404(stage)
        extra_qs['stage'] = pk
        filter_name = name
    elif year:
        extra_qs['year'] = get_object_or_404(Year, year=year)
        filter_name = extra_qs['year'].year
        description = extra_qs['year'].description
    else:
        if current:
            extra_qs['year'] = get_object_or_404(Year, default_year=True)
            filter_name = 'Current Year (' + extra_qs['year'].year + ')'
            description = extra_qs['year'].description
        else:
            extra_qs['year'] = get_object_or_404(Year, default_year=False)
            filter_name = 'Archive 2015'




    page_no = pagination.get_page_no(request.GET)
    object_list = (
        ActionCluster.objects.select_related('domain')
        .filter(**extra_qs).order_by('needs_partner'))
    featured_list = (ActionCluster.objects.select_related('domain')
                     .filter(is_featured=True, **extra_qs)[:3])
    page = pagination.get_page(object_list, page_no)
    context = {
        'featured_list': featured_list,
        'page': page,
        'domain_list': Domain.objects.all(),
        'stage_list': ActionCluster.STAGE_CHOICES,
        'filter_name': filter_name,
        'description': description,
        'current_domain': domain,
        'current_stage': int(stage) if stage else None,
        'appname': 'actionclusters',
    }
    return TemplateResponse(request, 'actionclusters/object_list.html', context)


def actioncluster_list_partner(request):
    """List action clusters looking for a partner."""
    extra_qs = {
        'is_approved': True,
        'status': ActionCluster.PUBLISHED,
        'needs_partner': True
    }
    page_no = pagination.get_page_no(request.GET)
    object_list = (
        ActionCluster.objects.select_related('domain').filter(**extra_qs))
    featured_list = (ActionCluster.objects.select_related('domain')
                     .filter(is_featured=True, **extra_qs)[:3])
    page = pagination.get_page(object_list, page_no)
    context = {
        'featured_list': featured_list,
        'page': page,
        'domain_list': Domain.objects.all(),
        'stage_list': ActionCluster.STAGE_CHOICES,
        'appname': 'actionclusters',
        'category': 'partner'
    }
    return TemplateResponse(request, 'actionclusters/object_list.html', context)


def actioncluster_list_iot(request):
    """List IOT project ideas."""
    extra_qs = {
        'is_approved': False,
        'status': ActionCluster.PUBLISHED,
    }
    page_no = pagination.get_page_no(request.GET)
    object_list = (
        ActionCluster.objects.select_related('domain').filter(**extra_qs))
    featured_list = (ActionCluster.objects.select_related('domain')
                     .filter(is_featured=True, **extra_qs)[:3])
    page = pagination.get_page(object_list, page_no)
    context = {
        'featured_list': featured_list,
        'page': page,
        'domain_list': Domain.objects.all(),
        'stage_list': ActionCluster.STAGE_CHOICES,
        'appname': 'actionclusters',
        'category': 'iot'
    }
    return TemplateResponse(request, 'actionclusters/object_list.html', context)


def get_actioncluster_for_user(slug, user):
    """Validates the user can access the given app."""
    actioncluster = get_object_or_404(ActionCluster.active, slug__exact=slug)
    # Application is published, no need for validation:
    if actioncluster.is_visible_by(user):
        return actioncluster
    raise Http404


def get_award_list(actioncluster):
    """Returns the list of awards for an app."""
    award_queryset = (ActionClusterAward.objects
                      .select_related('award').filter(actioncluster=actioncluster))
    return [a.award for a in award_queryset]


def get_hub_list(actioncluster):
    """Returns the list of hubs for an app."""
    hub_queryset = actioncluster.hubactionclustermembership_set.select_related('hub').all()
    return [h.hub for h in hub_queryset]


def actioncluster_detail(request, slug):
    actioncluster = get_actioncluster_for_user(slug, request.user)
    related_list = (ActionCluster.active.filter(domain=actioncluster.domain)
                    .order_by('?')[:3])
    context = {
        'object': actioncluster,
        'domain': actioncluster.domain,
        'community' : actioncluster.community,
        'url_list': actioncluster.actionclusterurl_set.all(),
        'media_list': actioncluster.actionclustermedia_set.all(),
        'feature_list': actioncluster.features.all(),
        'member_list': actioncluster.members.select_related('profile').all(),
        'hub_list': get_hub_list(actioncluster),
        'related_list': related_list,
        'award_list': get_award_list(actioncluster),
        'can_edit': actioncluster.is_editable_by(request.user),
        'is_owner': actioncluster.is_owned_by(request.user),
    }
    return TemplateResponse(request, 'actionclusters/object_detail.html', context)


# @login_required
def actioncluster_add(request):
    """View for adding an ``Application``."""
    if request.method == 'POST':
        form = ActionClusterForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.owner = request.user
            instance.save()
            form.save_m2m()
            mailer.notify_request(instance)
            messages.success(
                request, 'The action cluster "%s" has been added.' % instance.name)
            return redirect(instance.get_absolute_url())
    else:
        form = ActionClusterForm()
    context = {
        'form': form,
    }
    return TemplateResponse(request, 'actionclusters/object_add.html', context)


@login_required
def actioncluster_edit(request, slug):
    actioncluster = get_object_or_404(ActionCluster.active, slug__exact=slug)
    if not actioncluster.is_editable_by(request.user):
        raise Http404
    if request.method == 'POST':
        form = ActionClusterForm(
            request.POST, request.FILES, instance=actioncluster)
        link_formset = ActionClusterLinkFormSet(
            request.POST, instance=actioncluster)
        image_formset = ActionClusterMediaFormSet(
            request.POST, request.FILES, instance=actioncluster)
        if (form.is_valid() and link_formset.is_valid()
            and image_formset.is_valid()):
            instance = form.save()
            link_formset.save()
            image_formset.save()
            messages.success(
                request, 'The action cluster "%s" has been updated.'
                % instance.name)
            return redirect(instance.get_absolute_url())
    else:
        form = ActionClusterForm(instance=actioncluster)
        link_formset = ActionClusterLinkFormSet(instance=actioncluster)
        image_formset = ActionClusterMediaFormSet(instance=actioncluster)
    context = {
        'object': actioncluster,
        'form': form,
        'link_formset': link_formset,
        'image_formset': image_formset,
    }
    return TemplateResponse(request, 'actionclusters/object_edit.html', context)


def create_member(actioncluster, user):
    """Create a new member when it is unexistent and return it."""
    membership, is_new = (ActionClusterMembership.objects
                          .get_or_create(actioncluster=actioncluster, user=user))
    return membership if is_new else None


@login_required
def actioncluster_membership(request, slug):
    """Adds collaborators to an application."""
    actioncluster = get_object_or_404(
        ActionCluster.active, slug__exact=slug)
    if not actioncluster.is_owned_by(request.user):
        raise Http404
    if request.method == 'POST':
        form = MembershipForm(request.POST)
        formset = ActionClusterMembershipFormSet(
            request.POST, instance=actioncluster)
        if form.is_valid() and formset.is_valid():
            for member in form.cleaned_data['collaborators']:
                create_member(actioncluster, member)
            formset.save()
            messages.success(request, 'Membership successfully updated.')
            return redirect(actioncluster.get_membership_url())
    else:
        form = MembershipForm()
        formset = ActionClusterMembershipFormSet(instance=actioncluster)
    context = {
        'object': actioncluster,
        'form': form,
        'formset': formset,
    }
    return TemplateResponse(
        request, 'actionclusters/object_membership.html', context)


@login_required
def actioncluster_export(request, slug):
    """Generates an export of the current status of the application."""
    actioncluster = get_object_or_404(ActionCluster.active, slug__exact=slug)
    if not actioncluster.has_member(request.user):
        raise Http404
    context = {
        'object': actioncluster,
        'url_list': actioncluster.actionclusterurl_set.all(),
        'image_list': actioncluster.actionclustermedia_set.all(),
        'feature_list': actioncluster.features.all(),
        'member_list': actioncluster.members.select_related('profile').all(),

    }
    content = render_to_string('actionclusters/export.txt', context)
    response = HttpResponse(content, content_type='text/plain')
    filename = '%s-export-%s' % (
        actioncluster.slug, timezone.now().strftime("%Y%m%d-%H%M%S"))
    response['Content-Disposition'] = (
        'attachment; filename="%s.txt"' % filename)
    response['Content-Length'] = len(response.content)
    return response


def _get_membership_form(membership_list):
    id_list = [m.hub.id for m in membership_list]
    args = [{'hubs': id_list}] if id_list else []
    return HubActionClusterMembershipForm(*args)


def _update_membership(actioncluster, hub_list, membership_list):
    # Remove any non selected hub membership:
    for membership in membership_list:
        if membership.hub not in hub_list:
            membership.delete()
    # Add any new Hub membership:
    new_membership_list = []
    return [_add_hub_membership(hub, actioncluster) for hub in hub_list]


def _add_hub_membership(hub, actioncluster):
    """Generates the hub membership."""
    instance, is_new = HubActionClusterMembership.objects.get_or_create(
        hub=hub, actioncluster=actioncluster)
    # Record the activity for this membership.
    if is_new:
        name = ('Action cluster %s has been registered as part of this '
                'community.' % actioncluster.name)
        extra_data = {
            'url': actioncluster.get_absolute_url(),
            'user': actioncluster.owner,
        }
        hub.record_activity(name, extra_data=extra_data)
    return instance


@login_required
def actioncluster_hub_membership(request, slug):
    """View to manage the membership of an app to a hub."""
    actioncluster = get_object_or_404(ActionCluster.active, slug__exact=slug)
    if not actioncluster.is_editable_by(request.user):
        raise Http404
    # Determine existing membership:
    actioncluster_hubs = (actioncluster.hubactionclustermembership_set
                          .select_related('hub').all())
    if request.method == 'POST':
        form = HubActionClusterMembershipForm(request.POST)
        if form.is_valid():
            hubs = form.cleaned_data['hubs']
            _update_membership(actioncluster, hubs, actioncluster_hubs)
            msg = 'Hub membership updated.'
            messages.success(request, msg)
            return redirect(actioncluster.get_absolute_url())
    else:
        form = _get_membership_form(actioncluster_hubs)
    context = {
        'object': actioncluster,
        'form': form,
    }
    return TemplateResponse(
        request, 'actionclusters/object_hub_membership.html', context)
