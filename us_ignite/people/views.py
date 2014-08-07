from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404

from us_ignite.apps.models import Application
from us_ignite.awards.models import UserAward
from us_ignite.blog.models import Post
from us_ignite.common import pagination, forms
from us_ignite.events.models import Event
from us_ignite.hubs.models import Hub, HubMembership, HubRequest
from us_ignite.organizations.models import Organization, OrganizationMember
from us_ignite.profiles.models import Profile
from us_ignite.resources.models import Resource


PROFILE_SORTING_CHOICES = (
    ('', 'Select ordering'),
    ('user__first_name', 'Name a-z'),
    ('-user__first_name', 'Name z-a'),
)


@login_required
def profile_list(request):
    page_no = pagination.get_page_no(request.GET)
    order_form = forms.OrderForm(
        request.GET, order_choices=PROFILE_SORTING_CHOICES)
    order_value = order_form.cleaned_data['order'] if order_form.is_valid() else ''
    object_list = Profile.active.all()
    if order_value:
        # TODO consider using non case-sensitive ordering:
        object_list = object_list.order_by(order_value)
    page = pagination.get_page(object_list, page_no)
    context = {
        'page': page,
        'order': order_value,
        'order_form': order_form,
    }
    return TemplateResponse(request, 'people/object_list.html', context)


def get_application_list(owner, viewer=None):
    """Returns visible ``Applications`` from the given ``viewer``."""
    qs_kwargs = {'owner': owner}
    if not viewer or not owner == viewer:
        qs_kwargs.update({'status': Application.PUBLISHED})
    return Application.active.filter(**qs_kwargs)


def get_similar_applications(application_list, total=4):
    params = {
        'status': Application.PUBLISHED,
    }
    if application_list:
        application = application_list[0]
        params['domain'] = application.domain
        object_list =  (Application.active.filter(**params)
                        .exclude(owner=application.owner))
    else:
        object_list = Application.active.filter(**params)
    return object_list.order_by('?')[:total]


def get_event_list(user, viewer=None):
    """Returns visible ``Events`` from the given ``viewer``."""
    qs_kwargs = {'user': user}
    if not viewer or not user == viewer:
        qs_kwargs.update({'status': Event.PUBLISHED})
    return Event.objects.filter(**qs_kwargs)


def get_resource_list(contact, viewer=None):
    qs_kwargs = {'contact': contact}
    if not viewer or not contact == viewer:
        qs_kwargs.update({'status': Resource.PUBLISHED})
    return Resource.objects.filter(**qs_kwargs)


def get_hub_owned_list(contact, viewer=None):
    qs_kwargs = {'contact': contact}
    if not contact or not contact == viewer:
        qs_kwargs.update({'status': Hub.PUBLISHED})
    return Hub.objects.filter(**qs_kwargs)


def get_organization_list(user, viewer=None):
    qs_kwargs = {'user': user}
    if not user or not user == viewer:
        qs_kwargs.update({'organization__status': Organization.PUBLISHED})
    return (OrganizationMember.objects.select_related('organization')
            .filter(**qs_kwargs))


def get_hub_membership_list(user, viewer=None):
    qs_kwargs = {'user': user}
    if not user or not user == viewer:
        qs_kwargs.update({'hub__status': Hub.PUBLISHED})
    membership_list = (HubMembership.objects.select_related('hub')
                       .filter(**qs_kwargs))
    return [m.hub for m in membership_list]


def get_hub_list(user, viewer=None):
    hub_list = list(get_hub_owned_list(user, viewer=viewer))
    hub_list += get_hub_membership_list(user, viewer=viewer)
    return list(set(hub_list))


def get_featured_hub_list(limit=2):
    return (Hub.objects.filter(status=Hub.PUBLISHED, is_featured=True)
            .order_by('?')[:limit])


def get_award_list(user, viewer=None):
    qs_kwargs = {'user': user}
    award_qs = UserAward.objects.select_related('award').filter(**qs_kwargs)
    return [a.award for a in award_qs]


def get_post_list(limit=7):
    return (Post.published.all()
            .order_by('-is_featured', '-publication_date')[:limit])


def get_featured_resources(limit=2):
    return Resource.published.filter(is_featured=True)[:limit]

def get_featured_events(limit=2):
    return (Event.published.filter(is_featured=True)
            .order_by('?')[:limit])


@login_required
def profile_detail(request, slug):
    """Public profile of a user."""
    profile = get_object_or_404(
        Profile.active.select_related('user'), slug__exact=slug)
    user = profile.user
    is_owner = profile.user == request.user
    # Content available when the ``User`` owns this ``Profile``:
    hub_request_list = HubRequest.objects.filter(user=user) if is_owner else []
    context = {
        'object': profile,
        'is_owner': is_owner,
        'application_list': get_application_list(user, viewer=request.user),
        'event_list': get_event_list(user, viewer=request.user),
        'resource_list': get_resource_list(user, viewer=request.user),
        'hub_list': get_hub_list(user, viewer=request.user),
        'hub_request_list': hub_request_list,
        'organization_list': get_organization_list(user, viewer=request.user),
        'award_list': get_award_list(user, viewer=request.user),
    }
    return TemplateResponse(request, 'people/object_detail.html', context)


@login_required
def dashboard(request):
    profile, is_new = Profile.objects.get_or_create(user=request.user)
    user = profile.user
    application_list = list(get_application_list(user, viewer=request.user))
    similar_applications = get_similar_applications(application_list)
    event_list = get_event_list(user, viewer=request.user)
    resource_list = get_resource_list(user, viewer=request.user)
    content_list = (list(event_list) + list(resource_list))
    hub_list = get_hub_list(user, viewer=request.user)
    hub_id_list = [h.id for h in hub_list]
    context = {
        'object': profile,
        'application_list': application_list[:3],
        'similar_applications': similar_applications,
        'post_list': get_post_list(),
        'hub_list': hub_list[:7],
        'hub_event_list': Event.published.get_for_hubs(hub_id_list)[:6],
        'featured_event_list': get_featured_events(),
        'featured_hub_list': get_featured_hub_list(),
        'featured_resource_list': get_featured_resources(),
        'content_list': content_list,
        'hub_request_list': HubRequest.objects.filter(user=user)[:6],
    }
    return TemplateResponse(request, 'people/dashboard.html', context)
