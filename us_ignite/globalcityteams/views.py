from us_ignite.events.models import Event
from us_ignite.events.views import event_list as event_list_source


def event_list(request):
    """List the events for the global cities team."""
    response = event_list_source(request, section=Event.GLOBALCITIES)
    response.template_name = 'globalcityteams/event_list.html'
    return response
