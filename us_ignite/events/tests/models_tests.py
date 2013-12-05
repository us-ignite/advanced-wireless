import datetime
import pytz

from nose.tools import eq_, ok_

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from us_ignite.events import models
from us_ignite.events.tests import fixtures
from us_ignite.profiles.tests.fixtures import get_user


class TestEventModel(TestCase):

    def teatDown(self):
        for model in [models.Event, User]:
            model.objects.all().delete()

    def test_event_is_created_successfully(self):
        user = get_user('us-ignite')
        startdatetime = timezone.now()
        data = {
            'name': 'Gigabit community meet-up',
            'venue': 'London, UK',
            'start_datetime': startdatetime,
            'user': user,
        }
        instance = models.Event.objects.create(**data)
        ok_(instance.id)
        eq_(instance.name, 'Gigabit community meet-up'),
        ok_(instance.slug)
        eq_(instance.status, models.Event.DRAFT)
        eq_(instance.website, '')
        eq_(instance.image, '')
        eq_(instance.start_datetime, startdatetime)
        eq_(instance.end_datetime, None)
        eq_(instance.venue, 'London, UK')
        eq_(instance.description, '')
        eq_(list(instance.tags.all()), [])
        eq_(list(instance.hubs.all()), [])
        eq_(instance.user, user)
        eq_(instance.is_featured, False)
        eq_(instance.notes, '')
        ok_(instance.created)
        ok_(instance.modified)
        ok_(instance.position)

    def test_absolute_url_is_correct(self):
        user = get_user('us-ignite')
        event = fixtures.get_event(user=user)
        eq_(event.get_absolute_url(), '/event/%s/' % event.slug)

    def test_absolute_url_is_published(self):
        user = get_user('us-ignite')
        event = fixtures.get_event(user=user, status=models.Event.PUBLISHED)
        eq_(event.is_published(), True)

    def test_absolute_url_is_draft(self):
        user = get_user('us-ignite')
        event = fixtures.get_event(user=user, status=models.Event.DRAFT)
        eq_(event.is_draft(), True)

    def test_is_owner(self):
        user = get_user('us-ignite')
        event = fixtures.get_event(user=user)
        eq_(event.is_owner(user), True)

    def test_is_visible_by_owner(self):
        user = get_user('us-ignite')
        event = fixtures.get_event(user=user, status=models.Event.DRAFT)
        eq_(event.is_visible_by(user), True)

    def test_google_calendar_url_is_none(self):
        user = get_user('us-ignite')
        event = fixtures.get_event(user=user, status=models.Event.DRAFT)
        eq_(event.get_google_calendar_url(), None)

    def test_google_calendar_url_succeeds(self):
        user = get_user('us-ignite')
        ny_tz = pytz.timezone("America/New_York")
        start = ny_tz.localize(datetime.datetime(2013, 12, 2, 12, 00))
        end = ny_tz.localize(datetime.datetime(2013, 12, 2, 13, 00))
        event = fixtures.get_event(
            user=user, start_datetime=start, end_datetime=end)
        ok_(event.get_google_calendar_url())

    def test_ics_url_is_correct(self):
        user = get_user('us-ignite')
        event = fixtures.get_event(user=user)
        eq_(event.get_ics_url(), '/event/%s/ics/' % event.slug)
