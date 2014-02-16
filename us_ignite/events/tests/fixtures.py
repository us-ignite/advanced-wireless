from django.utils import timezone

from us_ignite.events.models import Audience, Event
from us_ignite.profiles.tests.fixtures import get_user


def get_audience(**kwargs):
    data = {'name': 'Develpoper'}
    data.update(kwargs)
    return Audience.objects.create(**data)


def get_event(**kwargs):
    data = {
        'name': 'Gigabit community meet-up',
        'venue': 'Washington, DC',
        'start_datetime': timezone.now(),
    }
    if not 'user' in kwargs:
        data['user'] = get_user('ignite-user')
    data.update(kwargs)
    return Event.objects.create(**data)
