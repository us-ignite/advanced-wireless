from us_ignite.hubs.models import Hub, HubRequest
from us_ignite.profiles.tests.fixtures import get_user


def get_hub(**kwargs):
    data = {
        'name': 'Local Community',
        'description': 'Gigabit local community',
    }
    data.update(kwargs)
    return Hub.objects.create(**data)


def get_hub_request(**kwargs):
    data = {
        'name': 'Local Community',
        'description': 'Gigabit local community',
    }
    if not 'user' in kwargs:
        data['user'] = get_user('user-community')
    data.update(**kwargs)
    return HubRequest.objects.create(**data)
