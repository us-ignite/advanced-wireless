from nose.tools import eq_

from django.contrib.auth.models import User
from django.test import TestCase

from us_ignite.events.tests import fixtures
from us_ignite.events.models import Event
from us_ignite.profiles.tests.fixtures import get_user


class TestEventPublishedManager(TestCase):

    def tearDown(self):
        for model in [Event, User]:
            model.objects.all().delete()

    def test_published_events_are_shown(self):
        user = get_user('ignite-user')
        event = fixtures.get_event(user=user, status=Event.PUBLISHED)
        eq_(list(Event.published.all()), [event])

    def test_unpublished_events_are_not_shown(self):
        user = get_user('ignite-user')
        event = fixtures.get_event(user=user, status=Event.DRAFT)
        eq_(list(Event.published.all()), [])
