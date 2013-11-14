from us_ignite.apps.models import Application, ApplicationMembership
from us_ignite.profiles.tests.fixtures import get_user


def get_application(**kwargs):
    defaults = {
        'name': 'Gigabit app',
    }
    if not 'owner' in kwargs:
        defaults['owner'] = get_user('us-ignite')
    defaults.update(kwargs)
    return Application.objects.create(**defaults)


def get_membership(application, user):
    membership, is_new = (ApplicationMembership.objects
                          .get_or_create(application=application, user=user))
    return membership
