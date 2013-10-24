from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404

from us_ignite.profiles.models import Profile
from us_ignite.common import pagination, forms


PROFILE_SORTING_CHOICES = (
    ('', 'Select ordering'),
    ('user__first_name', 'First name a-z'),
    ('-user__first_name', 'First name z-a'),
    ('user__last_name', 'Last name a-z'),
    ('-user__last_name', 'Last name z-a'),
)


@login_required
def profile_list(request):
    page_no = pagination.get_page_no(request.GET)
    order_form = forms.OrderForm(
        request.GET, order_choices=PROFILE_SORTING_CHOICES)
    order_value = order_form.cleaned_data['order'] if order_form.is_valid() else ''
    object_list = Profile.active.all()
    if order_value:
        object_list = object_list.order_by(order_value)
    page = pagination.get_page(object_list, page_no)
    context = {
        'page': page,
        'order': order_value,
        'order_form': order_form,
    }
    return render(request, 'people/object_list.html', context)


@login_required
def profile_detail(request, slug):
    """Public profile of a user."""
    profile = get_object_or_404(Profile.active, slug__exact=slug)
    context = {
        'object': profile,
    }
    return render(request, 'people/object_detail.html', context)
