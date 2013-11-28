from django.contrib.auth.decorators import login_required
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404

from us_ignite.apps.models import Application
from us_ignite.common import pagination, forms
from us_ignite.hubs.models import HubMembership
from us_ignite.profiles.models import Profile


PROFILE_SORTING_CHOICES = (
    ('', 'Select ordering'),
    ('name', 'Name a-z'),
    ('-name', 'Name z-a'),
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


def get_user_apps(owner, viewer=None):
    """Returns visible owned apps from the given ``User``."""
    qs_kwargs = {'owner': owner}
    # Only list public applications for this user.
    if not viewer or not owner == viewer:
        qs_kwargs.update({'status': Application.PUBLISHED})
    return Application.active.filter(**qs_kwargs)


@login_required
def profile_detail(request, slug):
    """Public profile of a user."""
    profile = get_object_or_404(
        Profile.active.select_related('user'), slug__exact=slug)
    app_list = get_user_apps(profile.user, viewer=request.user)
    membership_list = (HubMembership.objects.select_related('hub')
                       .filter(user=profile.user))
    context = {
        'object': profile,
        'app_list': app_list,
        'membership_list': membership_list,
    }
    return TemplateResponse(request, 'people/object_detail.html', context)
