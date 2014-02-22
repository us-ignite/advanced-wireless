from us_ignite.resources.models import Resource


def get_resource(**kwargs):
    data = {
        'name': 'Gigabit resource',
        'description': 'Gigabit description',
    }
    data.update(kwargs)
    return Resource.objects.create(**kwargs)
