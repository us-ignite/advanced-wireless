from us_ignite.hubs.models import Hub


def create_hub(**kwargs):
    data = {
        'name': 'Local Community',
        'description': 'Gigabit local community',
    }
    data.update(kwargs)
    return Hub.objects.create(**data)
