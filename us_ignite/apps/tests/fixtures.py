from us_ignite.apps.models import (Application, ApplicationMembership,
                                   Domain, Page)
from us_ignite.profiles.tests.fixtures import get_user


def get_application(**kwargs):
    data = {
        'name': 'Gigabit app',
    }
    if not 'owner' in kwargs:
        data['owner'] = get_user('us-ignite')
    data.update(kwargs)
    return Application.objects.create(**data)


def get_membership(application, user):
    membership, is_new = (ApplicationMembership.objects
                          .get_or_create(application=application, user=user))
    return membership


def get_page(**kwargs):
    data = {
        'name': 'Application list',
    }
    data.update(kwargs)
    return Page.objects.create(**data)


def get_domain(**kwargs):
    data = {
        'name': 'Healthcare',
        'slug': 'healthcare',
    }
    data.update(kwargs)
    return Domain.objects.create(**data)
