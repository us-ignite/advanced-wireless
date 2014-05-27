from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from us_ignite.common import pagination
from us_ignite.common.response import json_response
from us_ignite.maps.utils import get_location_dict
from us_ignite.testbeds.models import Testbed


def testbed_detail(request, slug):
    """Detail of a ``testbed``."""
    instance = get_object_or_404(
        Testbed.objects.select_related('contact'), slug__exact=slug)
    if not instance.is_visible_by(request.user):
        raise Http404
    context = {
        'object': instance,
        'is_editable': instance.is_editable_by(request.user),
        'app_list': instance.applications.all(),
    }
    return TemplateResponse(request, 'testbed/object_detail.html', context)


def testbed_list(request):
    """List of all the testbeds."""
    page_no = pagination.get_page_no(request.GET)
    object_list = Testbed.active.all()
    page = pagination.get_page(object_list, page_no)
    context = {
        'page': page,
    }
    return TemplateResponse(request, 'testbed/object_list.html', context)


def get_app_list(testbed):
    return [get_location_dict(a, 'app') for a in testbed.applications.all()]


def testbed_locations_json(request, slug):
    testbed = get_object_or_404(Testbed.active, slug__exact=slug)
    item_list =[get_location_dict(testbed, 'testbed')]
    item_list += get_app_list(testbed)
    return json_response(item_list, callback='map.render')
