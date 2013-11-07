from us_ignite.apps.models import Application
from us_ignite.profiles.tests.fixtures import get_user


def get_application(**kwargs):
    defaults = {
        'name': 'Gigabit app',
    }
    if not 'owner' in kwargs:
        defaults['owner'] = get_user('us-ignite')
    defaults.update(kwargs)
    return Application.objects.create(**defaults)
