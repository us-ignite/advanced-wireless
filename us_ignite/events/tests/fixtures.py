from us_ignite.events.models import Event

from us_ignite.profiles.tests.fixtures import get_user


def get_event(**kwargs):
    data = {
        'name': 'Gigabit community meet-up',
        'venue': 'Washington, DC',
    }
    if not 'user' in kwargs:
        data['user'] = get_user('ignite-user')
    data.update(kwargs)
    return Event.objects.create(**data)
