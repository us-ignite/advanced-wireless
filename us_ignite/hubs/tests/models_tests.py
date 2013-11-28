from nose.tools import eq_, ok_

from django.contrib.auth.models import User
from django.test import TestCase

from us_ignite.profiles.tests.fixtures import get_user
from us_ignite.hubs.models import Hub, HubActivity, HubMembership, HubRequest
from us_ignite.hubs.tests import fixtures


class TestHubRequestModel(TestCase):

    def tearDown(self):
        for model in [HubRequest, User]:
            model.objects.all().delete()

    def test_model_can_be_created_successfully(self):
        user = get_user('us-ignite')
        data = {
            'name': 'Local Community',
            'description': 'Gigabit local community',
            'user': user,
        }
        instance = HubRequest.objects.create(**data)
        ok_(instance.id)
        eq_(instance.name, 'Local Community')
        eq_(instance.user, user)
        eq_(instance.summary, '')
        eq_(instance.description, 'Gigabit local community')
        eq_(instance.website, '')
        ok_(instance.created)
        ok_(instance.modified)

    def test_admin_url(self):
        user = get_user('us-ignite')
        instance = fixtures.get_hub_request(user=user)
        eq_(instance.get_admin_url(),
            '/admin/hubs/hubrequest/%s/' % instance.id)


class TestHubModel(TestCase):

    def tearDown(self):
        for model in [Hub, User]:
            model.objects.all().delete()

    def test_model_can_be_created_successfully(self):
        data = {
            'name': 'Local Community',
            'description': 'Gigabit local community',
        }
        instance = Hub.objects.create(**data)
        ok_(instance.id)
        eq_(instance.name, 'Local Community')
        eq_(instance.slug, 'local-community')
        eq_(instance.guardian, None)
        eq_(instance.summary, '')
        eq_(instance.description, 'Gigabit local community')
        eq_(instance.image, '')
        eq_(instance.website, '')
        ok_(instance.created)
        ok_(instance.modified)
        eq_(list(instance.features.all()), [])
        eq_(list(instance.tags.all()), [])

    def test_is_guardian(self):
        guardian = get_user('guardian')
        instance = fixtures.get_hub(guardian=guardian)
        eq_(instance.is_guardian(guardian), True)

    def test_is_published(self):
        guardian = get_user('guardian')
        instance = fixtures.get_hub(guardian=guardian, status=Hub.PUBLISHED)
        eq_(instance.is_published(), True)

    def test_get_absolute_url(self):
        guardian = get_user('guardian')
        instance = fixtures.get_hub(guardian=guardian)
        eq_(instance.get_absolute_url(), '/hub/%s/' % instance.slug)


class TestHubActivityModel(TestCase):

    def tearDown(self):
        for model in [Hub]:
            model.objects.all().delete()

    def create_hub_activity_is_successful(self):
        hub = fixtures.create_hub('Gigabit hub')
        data = {
            'hub': hub,
            'title': 'New app added!',
        }
        instance = HubActivity.objects.craete(**data)
        ok_(instance.id)
        eq_(instance.hub, hub)
        eq_(instance.title, 'New app added!')
        eq_(instance.description, '')
        eq_(instance.url, '')
        eq_(instance.user, None)
        ok_(instance.created)
        ok_(instance.modified)


class TestHubMembershipModel(TestCase):

    def tearDown(self):
        for model in [Hub, User]:
            model.objects.all().delete()

    def test_create_membership(self):
        user = get_user('member')
        hub = fixtures.get_hub(status=Hub.PUBLISHED)
        data = {
            'hub': hub,
            'user': user,
        }
        instance = HubMembership.objects.create(**data)
        ok_(instance.id)
        eq_(instance.hub, hub)
        eq_(instance.user, user)
        ok_(instance.created)
