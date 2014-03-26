from nose.tools import ok_, eq_

from django.contrib.auth.models import User
from django.test import TestCase

from us_ignite.common.tests import utils
from us_ignite.resources.models import Resource, ResourceType, Sector
from us_ignite.resources.tests import fixtures
from us_ignite.profiles.tests.fixtures import get_user


class TestResourceModel(TestCase):

    def tearDown(self):
        for model in [Resource, User]:
            model.objects.all().delete()

    def test_resource_creation(self):
        data = {
            'name': 'Gigabit resource',
            'description': 'Gigabit description',
        }
        instance = Resource.objects.create(**data)
        ok_(instance.id)
        eq_(instance.name, 'Gigabit resource')
        ok_(instance.slug)
        eq_(instance.status, Resource.DRAFT)
        eq_(instance.url, '')
        eq_(instance.description, 'Gigabit description')
        eq_(instance.resource_type, None)
        eq_(instance.sector, None)
        eq_(instance.contact, None)
        eq_(instance.author, '')
        eq_(instance.organization, None)
        eq_(instance.image, '')
        eq_(instance.asset, '')
        eq_(instance.is_featured, False)
        eq_(instance.resource_date, None)
        eq_(list(instance.tags.all()), [])
        ok_(instance.created)
        ok_(instance.modified)

    def test_is_visible(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(contact=user, status=Resource.PUBLISHED)
        eq_(resource.is_published(), True)

    def test_unpublished_resource_is_not_visible(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(contact=user, status=Resource.DRAFT)
        eq_(resource.is_visible_by(utils.get_anon_mock()), False)

    def test_visible_resource_is_published(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(contact=user, status=Resource.PUBLISHED)
        eq_(resource.is_visible_by(utils.get_anon_mock()), True)

    def unpublished_resource_can_be_viewed_by_owner(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(contact=user, status=Resource.DRAFT)
        eq_(resource.is_visible_by(user), True)

    def test_get_absolute_url(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(contact=user, slug='foo')
        eq_(resource.get_absolute_url(), '/resources/foo/')

    def test_get_edit_url(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(contact=user, slug='foo')
        eq_(resource.get_edit_url(), '/resources/foo/edit/')

    def test_get_resource_url(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(
            contact=user, url='http://us-ignite.org')
        eq_(resource.get_resource_url(), 'http://us-ignite.org')

    def test_empty_resource_url(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(contact=user)
        eq_(resource.get_resource_url(), '')

    def test_resource_is_draft(self):
        resource = fixtures.get_resource(status=Resource.DRAFT)
        eq_(resource.is_draft(), True)

    def test_user_is_owner(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(contact=user)
        eq_(resource.is_editable_by(user), True)

    def test_resource_allows_null_contact(self):
        resource = fixtures.get_resource(contact=None)
        ok_(resource.id)
        eq_(resource.contact, None)

    def test_ownerless_resource_is_not_editable(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(contact=None)
        ok_(not resource.is_editable_by(user))
        ok_(not resource.is_editable_by(utils.get_anon_mock()))


class TestResourceTypeModel(TestCase):

    def tearDown(self):
        ResourceType.objects.all().delete()

    def test_resource_type_can_be_created_successfully(self):
        data = {
            'name': 'Video'
        }
        instance = ResourceType.objects.create(**data)
        ok_(instance.id)
        eq_(instance.name, 'Video')
        eq_(instance.slug, 'video')


class TestSectorModel(TestCase):

    def tearDown(self):
        Sector.objects.all().delete()

    def test_sector_can_be_created_successfully(self):
        data = {
            'name': 'Public Safety'
        }
        instance = Sector.objects.create(**data)
        ok_(instance.id)
        eq_(instance.name, 'Public Safety')
        eq_(instance.slug, 'public-safety')
