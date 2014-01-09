from nose.tools import ok_, eq_

from django.contrib.auth.models import User
from django.test import TestCase

from us_ignite.common.tests import utils
from us_ignite.resources.models import Resource
from us_ignite.resources.tests import fixtures
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

    def test_is_visible(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(owner=user, status=Resource.PUBLISHED)
        eq_(resource.is_published(), True)

    def test_unpublished_resource_is_not_visible(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(owner=user, status=Resource.DRAFT)
        eq_(resource.is_visible_by(utils.get_anon_mock()), False)

    def test_visible_resource_is_published(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(owner=user, status=Resource.PUBLISHED)
        eq_(resource.is_visible_by(utils.get_anon_mock()), True)

    def unpublished_resource_can_be_viewed_by_owner(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(owner=user, status=Resource.DRAFT)
        eq_(resource.is_visible_by(user), True)
