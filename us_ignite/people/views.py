from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from us_ignite.profiles.models import Profile
from us_ignite.common import pagination


@login_required
def people_list(request):
    page_no = pagination.get_page_no(request.GET)
    order_value = pagination.get_order_value(
        request.GET, ['user__first_name', 'user__last_name'])
    object_list = Profile.active.all()
    if order_value:
        object_list = object_list.order_by(order_value)
    page = pagination.get_page(object_list, page_no)
    context = {
        'page': page,
        'order': order_value,
    }
    return render(request, 'people/object_list.html', context)
