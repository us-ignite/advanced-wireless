from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse

from us_ignite.common import pagination
from us_ignite.common.response import json_response
from us_ignite.maps.utils import get_location_dict
from us_ignite.testbeds.models import Testbed
from us_ignite.testbeds.forms import TestbedFilterForm


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


def get_testbed_query(data):
    """Transform cleaned data in Testbed."""
    query = {}
    for key, value in data.items():
        if key.startswith('passes_'):
            key = '%s__gte' % key
        if value:
            query[key] = value
    return query


def testbed_list(request):
    """List of all the testbeds."""
    testbed_query = {}
    if request.GET:
        form = TestbedFilterForm(request.GET)
        if form.is_valid():
            testbed_query = get_testbed_query(form.cleaned_data)
    else:
        form = TestbedFilterForm()
    page_no = pagination.get_page_no(request.GET)
    object_list = Testbed.active.filter(**testbed_query)
    page = pagination.get_page(object_list, page_no)
    context = {
        'page': page,
        'form': form,
    }
    return TemplateResponse(request, 'testbed/object_list.html', context)


def get_app_list(testbed):
    return [get_location_dict(a, 'app') for a in testbed.applications.all()]


def testbed_locations_json(request, slug):
    testbed = get_object_or_404(Testbed.active, slug__exact=slug)
    item_list =[get_location_dict(testbed, 'testbed')]
    item_list += get_app_list(testbed)
    return json_response(item_list, callback='map.render')
