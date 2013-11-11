from nose.tools import eq_, ok_

from django.contrib.auth.models import User, AnonymousUser
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

    def test_application_absolute_url(self):
        user = get_user('app-owner')
        application = fixtures.get_application(owner=user)
        eq_(application.get_absolute_url(), u'/apps/%s/' % application.slug)

    def test_application_is_public(self):
        user = get_user('app-owner')
        application = fixtures.get_application(
            owner=user, status=models.Application.PUBLISHED)
        ok_(application.is_public())

    def test_application_is_draft(self):
        user = get_user('app-owner')
        application = fixtures.get_application(
            owner=user, status=models.Application.DRAFT)
        ok_(application.is_draft())

    def test_application_ownership(self):
        user = get_user('app-owner')
        application = fixtures.get_application(owner=user)
        ok_(application.is_owned_by(user))

    def test_application_owner_membership(self):
        user = get_user('app-owner')
        application = fixtures.get_application(owner=user)
        ok_(application.has_member(user))

    def test_application_member_membership(self):
        user = get_user('app-owner')
        member = get_user('app-member')
        application = fixtures.get_application(owner=user)
        models.ApplicationMembership.objects.create(
            application=application, user=member)
        ok_(application.has_member(member))

    def test_published_app_is_visible_by_anon(self):
        user = get_user('app-owner')
        application = fixtures.get_application(
            owner=user, status=models.Application.PUBLISHED)
        ok_(application.is_visible_by(AnonymousUser()))

    def test_draft_app_is_visible_by_owner(self):
        user = get_user('app-owner')
        application = fixtures.get_application(
            owner=user, status=models.Application.DRAFT)
        ok_(application.is_visible_by(user))

    def test_draft_app_is_visible_by_member(self):
        user = get_user('app-owner')
        member = get_user('app-member')
        application = fixtures.get_application(
            owner=user, status=models.Application.DRAFT)
        models.ApplicationMembership.objects.create(
            application=application, user=member)
        ok_(application.is_visible_by(member))

    def test_app_is_editable_by_owner(self):
        user = get_user('app-owner')
        application = fixtures.get_application(
            owner=user, status=models.Application.DRAFT)
        ok_(application.is_editable_by(user))

    def test_app_is_editable_by_other_user(self):
        user = get_user('app-owner')
        member = get_user('app-member')
        application = fixtures.get_application(
            owner=user, status=models.Application.DRAFT)
        eq_(application.is_editable_by(member), False)

    def test_app_is_not_editable_by_anon(self):
        user = get_user('app-owner')
        application = fixtures.get_application(
            owner=user, status=models.Application.DRAFT)
        eq_(application.is_editable_by(AnonymousUser()), False)


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
