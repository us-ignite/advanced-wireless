from nose.tools import eq_, ok_

from django.contrib.auth.models import User
from django.test import TestCase

from us_ignite.apps.models import Application
from us_ignite.apps.tests.fixtures import get_application
from us_ignite.awards.models import Award, ApplicationAward, HubAward, UserAward
from us_ignite.awards.tests import fixtures
from us_ignite.hubs.models import Hub
from us_ignite.hubs.tests.fixtures import get_hub
from us_ignite.profiles.tests.fixtures import get_user


class TestAwardModel(TestCase):

    def tearDown(self):
        for model in [Award]:
            model.objects.all().delete()

    def test_create_award_is_successful(self):
        data = {
            'name': 'Gold star',
        }
        instance = Award.objects.create(**data)
        ok_(instance.id)
        eq_(instance.name, 'Gold star')
        ok_(instance.slug)
        eq_(instance.description, '')
        eq_(instance.image, '')


class TestApplicationAwardModel(TestCase):

    def tearDown(self):
        for model in [Award, Application, User]:
            model.objects.all().delete()

    def test_application_award_creation_is_successful(self):
        user = get_user('us-ignite')
        application = get_application(owner=user)
        award = fixtures.get_award(name='Gold star')
        data = {
            'application': application,
            'award': award,
        }
        instance = ApplicationAward.objects.create(**data)
        ok_(instance.id)
        ok_(instance.created)
        eq_(instance.application, application)
        eq_(instance.award, award)


class TestHubAwardModel(TestCase):

    def tearDown(self):
        for model in [Award, Hub, User]:
            model.objects.all().delete()

    def test_hub_award_creation_is_successful(self):
        user = get_user('us-ignite')
        hub = get_hub()
        award = fixtures.get_award(name='Gold star')
        data = {
            'hub': hub,
            'award': award,
        }
        instance = HubAward.objects.create(**data)
        ok_(instance.id)
        ok_(instance.created)
        eq_(instance.hub, hub)
        eq_(instance.award, award)


class TestUserAwardModel(TestCase):

    def tearDown(self):
        for model in [Award, User]:
            model.objects.all().delete()

    def test_hub_award_creation_is_successful(self):
        user = get_user('us-ignite')
        award = fixtures.get_award(name='Gold star')
        data = {
            'user': user,
            'award': award,
        }
        instance = UserAward.objects.create(**data)
        ok_(instance.id)
        ok_(instance.created)
        eq_(instance.user, user)
        eq_(instance.award, award)
