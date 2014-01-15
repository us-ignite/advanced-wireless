from django.views.decorators.csrf import csrf_exempt

from us_ignite.apps.models import Application
from us_ignite.events.models import Event
from us_ignite.search.filters import tag_search


@csrf_exempt
def search_apps(request):
    return tag_search(
        request, Application.active, 'search/application_list.html')


@csrf_exempt
def search_events(request):
    return tag_search(
        request, Event.published, 'search/event_list.html')