from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from us_ignite.profiles.models import Profile
from us_ignite.common import pagination


@login_required
def people_list(request):
    object_list = Profile.active.all()
    page_no = pagination.get_page_no(request.GET)
    page = pagination.get_page(object_list, page_no)
    context = {
        'page': page,
    }
    return render(request, 'people/object_list.html', context)
