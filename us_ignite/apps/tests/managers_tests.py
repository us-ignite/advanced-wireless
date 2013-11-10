from nose.tools import eq_

from django.contrib.auth.models import User
from django.test import TestCase

from us_ignite.apps.models import Application
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
