from nose.tools import eq_, ok_

from django.contrib.auth.models import User
from django.test import TestCase

from us_ignite.apps.models import Application
from us_ignite.apps.tests.fixtures import get_application
from us_ignite.badges.models import Badge, ApplicationBadge
from us_ignite.badges.tests import fixtures
from us_ignite.profiles.tests.fixtures import get_user


class TestBadgeModel(TestCase):

    def tearDown(self):
        for model in [Badge]:
            model.objects.all().delete()

    def test_create_badge_is_successful(self):
        data = {
            'name': 'Gold star',
        }
        instance = Badge.objects.create(**data)
        ok_(instance.id)
        eq_(instance.name, 'Gold star')
        ok_(instance.slug)
        eq_(instance.description, '')
        eq_(instance.image, '')


class TestApplicationBadgeModel(TestCase):

    def tearDown(self):
        for model in [Badge, Application, User]:
            model.objects.all().delete()

    def test_application_badge_creation_is_successful(self):
        user = get_user('us-ignite')
        application = get_application(owner=user)
        badge = fixtures.get_badge(name='Gold star')
        data = {
            'application': application,
            'badge': badge,
        }
        instance = ApplicationBadge.objects.create(**data)
        ok_(instance.id)
