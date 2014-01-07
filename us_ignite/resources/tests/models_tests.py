from nose.tools import ok_, eq_

from django.contrib.auth.models import User
from django.test import TestCase

from us_ignite.resources.models import Resource
from us_ignite.profiles.tests.fixtures import get_user


class TestResourceModel(TestCase):

    def tearDown(self):
        for model in [Resource, User]:
            model.objects.all().delete()

    def test_resource_creation(self):
        user = get_user('us-ignite')
        data = {
            'name': 'Gigabit resource',
            'owner': user,
        }
        instance = Resource.objects.create(**data)
        ok_(instance.id)
        ok_(instance.slug)
        eq_(instance.status, Resource.DRAFT)
        eq_(instance.description, '')
        eq_(instance.owner, user)
        eq_(instance.organization, None)
        eq_(instance.url, '')
        eq_(instance.asset, '')
        eq_(instance.is_featured, False)
        eq_(list(instance.tags.all()), [])
        ok_(instance.created)
        ok_(instance.modified)
