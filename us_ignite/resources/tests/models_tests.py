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

    def test_get_absolute_url(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(owner=user, slug='foo')
        eq_(resource.get_absolute_url(), '/resources/foo/')

    def test_get_edit_url(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(owner=user, slug='foo')
        eq_(resource.get_edit_url(), '/resources/foo/edit/')

    def test_get_resource_url(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(
            owner=user, url='http://us-ignite.org')
        eq_(resource.get_resource_url(), 'http://us-ignite.org')

    def test_empty_resource_url(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(owner=user)
        eq_(resource.get_resource_url(), '')

    def test_user_is_owner(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(owner=user)
        eq_(resource.is_owner(user), True)

    def test_resource_avoids_ownership(self):
        resource = fixtures.get_resource(owner=None)
        ok_(resource.id)
        eq_(resource.owner, None)

    def test_ownerless_resource_has_no_owner(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(owner=None)
        ok_(not resource.is_owner(user))
        ok_(not resource.is_owner(utils.get_anon_mock()))
