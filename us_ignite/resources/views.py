from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from us_ignite.common import pagination
from us_ignite.resources.models import Resource


def resource_detail(request, slug):
    resource = get_object_or_404(Resource, slug__exact=slug)
    if not resource.is_visible_by(request.user):
        raise Http404
    context = {
        'object': resource,
    }
    return TemplateResponse(request, 'resources/object_detail.html', context)


def resource_list(request):
    page_no = pagination.get_page_no(request.GET)
    object_list = Resource.objects.filter(status=Resource.PUBLISHED)
    page = pagination.get_page(object_list, page_no)
    context = {
        'page': page,
    }
    return TemplateResponse(request, 'resources/object_list.html', context)
