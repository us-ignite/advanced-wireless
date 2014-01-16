from django.views.decorators.csrf import csrf_exempt

from us_ignite.apps.models import Application
from us_ignite.events.models import Event
from us_ignite.hubs.models import Hub
from us_ignite.organizations.models import Organization
from us_ignite.search.filters import tag_search


@csrf_exempt
def search_apps(request):
    return tag_search(
        request, Application.active, 'search/application_list.html')


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
