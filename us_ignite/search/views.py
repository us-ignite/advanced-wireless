import watson

from django.template.response import TemplateResponse
from django.utils.http import urlencode
from django.views.decorators.csrf import csrf_exempt

from us_ignite.apps.models import Application
from us_ignite.common import pagination
from us_ignite.events.models import Event
from us_ignite.hubs.models import Hub
from us_ignite.organizations.models import Organization
from us_ignite.resources.models import Resource
from us_ignite.search.filters import tag_search
from us_ignite.search.forms import SearchForm


@csrf_exempt
def search_apps(request):
    return tag_search(
        request, Application.active.filter(status=Application.PUBLISHED),
        'search/application_list.html')


@csrf_exempt
def search_events(request):
    return tag_search(request, Event.published, 'search/event_list.html')


@csrf_exempt
def search_hubs(request):
    return tag_search(request, Hub.active, 'search/hub_list.html')


@csrf_exempt
def search_organizations(request):
    return tag_search(
        request, Organization.active, 'search/organization_list.html')


@csrf_exempt
def search_resources(request):
    return tag_search(
        request, Resource.published, 'search/resource_list.html')


@csrf_exempt
def search(request):
    form = SearchForm(request.GET) if 'q' in request.GET else SearchForm()
    page_no = pagination.get_page_no(request.GET)
    if form.is_valid():
        object_list = watson.search(form.cleaned_data['q'])
        pagination_qs = '&%s' % urlencode({'q': form.cleaned_data['q']})
    else:
        object_list = []
        pagination_qs = ''
    page = pagination.get_page(object_list, page_no)
    context = {
        'form': form,
        'page': page,
        'pagination_qs': pagination_qs,
    }
    return TemplateResponse(request, 'search/object_list.html', context)
