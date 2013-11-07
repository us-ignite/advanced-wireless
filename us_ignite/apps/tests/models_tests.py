from nose.tools import eq_, ok_

from django.contrib.auth.models import User
from django.test import TestCase

from us_ignite.apps import models
from us_ignite.apps.tests import fixtures
from us_ignite.profiles.tests.fixtures import get_user


class ApplicationTest(TestCase):

    def tearDown(self):
        for model in [User, models.Application]:
            model.objects.all().delete()

    def test_application_creation_is_successful(self):
        user = get_user('us-ignite')
        data = {
            'name': 'Gigabit app',
            'owner': user,
        }
        instance = models.Application.objects.create(**data)
        eq_(instance.name, 'Gigabit app')
        ok_(instance.slug)
        eq_(instance.owner, user)
        eq_(instance.status, models.Application.DRAFT)
        ok_(instance.created)
        ok_(instance.modified)
        eq_(instance.description, '')
        eq_(instance.assistance, '')
        eq_(instance.technology, '')
        eq_(list(instance.members.all()), [])
        eq_(list(instance.tags.all()), [])


class TestApplicationMembership(TestCase):

    def tearDown(self):
        for model in [User, models.Application, models.ApplicationMembership]:
            model.objects.all().delete()

    def test_application_membership_creation(self):
        user = get_user('app-owner')
        member = get_user('member')
        application = fixtures.get_application(owner=user)
        data = {
            'user': member,
            'application': application,
        }
        instance = models.ApplicationMembership.objects.create(**data)
        eq_(instance.user, member)
        eq_(instance.application, application)
        ok_(instance.created)


class TestApplicationURL(TestCase):

    def tearDown(self):
        for model in [User, models.Application, models.ApplicationURL]:
            model.objects.all().delete()

    def test_application_url_creation(self):
        user = get_user('app-owner')
        application = fixtures.get_application(owner=user)
        data = {
            'application': application,
            'url': 'http://us-ignite.org',
        }
        instance = models.ApplicationURL.objects.create(**data)
        eq_(instance.application, application)
        eq_(instance.name, '')
        eq_(instance.url, 'http://us-ignite.org')