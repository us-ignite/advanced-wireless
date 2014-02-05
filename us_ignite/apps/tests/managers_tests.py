from nose.tools import eq_, ok_

from django.contrib.auth.models import User
from django.test import TestCase

from us_ignite.apps.models import Application, ApplicationVersion
from us_ignite.apps.tests import fixtures
from us_ignite.profiles.tests.fixtures import get_user


class TestApplicationActiveManager(TestCase):

    def tearDown(self):
        for model in [User, Application]:
            model.objects.all().delete()

    def test_active_application_is_returned(self):
        user = get_user('app-owner')
        application = fixtures.get_application(
            owner=user, status=Application.DRAFT)
        queryset = Application.active.all()
        eq_(list(queryset), [application])

    def test_removed_application_is_not_returned(self):
        user = get_user('app-owner')
        fixtures.get_application(owner=user, status=Application.REMOVED)
        queryset = Application.active.all()
        eq_(list(queryset), [])


class TestApplicationPublishedManager(TestCase):

    def tearDown(self):
        for model in [User, Application]:
            model.objects.all().delete()

    def test_published_application_is_returned(self):
        user = get_user('app-owner')
        application = fixtures.get_application(
            owner=user, status=Application.PUBLISHED)
        queryset = Application.published.all()
        eq_(list(queryset), [application])

    def test_draft_application_is_not_returned(self):
        user = get_user('app-owner')
        fixtures.get_application(owner=user, status=Application.DRAFT)
        queryset = Application.published.all()
        eq_(list(queryset), [])


class TestApplicationVersionManager(TestCase):

    def tearDown(self):
        for model in [User, Application]:
            model.objects.all().delete()

    def test_active_application_is_duplicated(self):
        user = get_user('app-owner')
        application = fixtures.get_application(owner=user)
        version = ApplicationVersion.objects.create_version(application)
        ok_(version.id)
        ok_(not version.slug == application.slug)
        eq_(version.application, application)
        eq_(version.name, application.name)
        eq_(version.website, application.website)
        eq_(version.stage, application.stage)
        eq_(version.image, application.image)
        eq_(version.summary, application.summary)
        eq_(version.impact_statement, application.impact_statement)
        eq_(version.description, application.description)
        eq_(version.roadmap, application.roadmap)
        eq_(version.assistance, application.assistance)
        eq_(version.team_description, application.team_description)
        eq_(version.acknowledgments, application.acknowledgments)
        eq_(version.notes, application.notes)

    def test_missing_latest_version_returns_none(self):
        user = get_user('app-owner')
        application = fixtures.get_application(owner=user)
        result = ApplicationVersion.objects.get_latest_version(application)
        eq_(result, None)

    def test_latest_version_is_returned_successfullly(self):
        user = get_user('app-owner')
        application = fixtures.get_application(owner=user)
        version = ApplicationVersion.objects.create_version(application)
        result = ApplicationVersion.objects.get_latest_version(application)
        eq_(result, version)

