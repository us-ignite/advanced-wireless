import datetime
import pytz

from nose.tools import eq_, ok_

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from us_ignite.events import models
from us_ignite.events.tests import fixtures
from us_ignite.profiles.tests.fixtures import get_user


class TestAudienceModel(TestCase):

    def test_audience_is_created_successfully(self):
        data = {'name': 'Developer'}
        instance = models.Audience.objects.create(**data)
        ok_(instance.id)
        eq_(instance.name, 'Developer')
        eq_(instance.slug, 'developer')


class TestEventModel(TestCase):

    def tearDown(self):
        for model in [models.Event, User]:
            model.objects.all().delete()

    def test_event_is_created_successfully(self):
        user = get_user('us-ignite')
        startdatetime = timezone.now()
        data = {
            'name': 'Gigabit community meet-up',
            'address': 'London, UK',
            'start_datetime': startdatetime,
            'user': user,
        }
        instance = models.Event.objects.create(**data)
        ok_(instance.id)
        eq_(instance.name, 'Gigabit community meet-up')
        ok_(instance.slug)
        eq_(instance.status, models.Event.PUBLISHED)
        eq_(instance.image, '')
        eq_(instance.description, '')
        eq_(instance.start_datetime, startdatetime)
        eq_(instance.end_datetime, None)
        eq_(instance.address, 'London, UK')
        eq_(instance.contact, None)
        eq_(instance.scope, models.Event.NATIONAL)
        eq_(list(instance.audiences.all()), [])
        eq_(instance.website, '')
        eq_(instance.tickets_url, '')
        eq_(list(instance.tags.all()), [])
        eq_(list(instance.hubs.all()), [])
        eq_(instance.user, user)
        eq_(instance.is_featured, False)
        eq_(instance.is_ignite, False)
        eq_(instance.notes, '')
        ok_(instance.created)
        ok_(instance.modified)
        ok_(instance.position)
        eq_(instance.audience_other, '')

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

    def test_edit_url_is_correct(self):
        user = get_user('us-ignite')
        event = fixtures.get_event(user=user)
        eq_(event.get_edit_url(), '/event/%s/edit/' % event.slug)

    def test_event_can_be_userless(self):
        event = fixtures.get_event(user=None)
        ok_(event.id)
        eq_(event.user, None)

    def test_userless_event_is_not_owned(self):
        user = get_user('us-ignite')
        event = fixtures.get_event(user=None)
        eq_(event.is_owner(user), False)

    def test_get_location_dict(self):
        user = get_user('us-ignite')
        event = fixtures.get_event(user=user)
        eq_(sorted(event.get_location_dict().keys()),
            sorted(['type', 'latitude', 'longitude', 'name', 'website',
                    'content', 'category', 'image']))


class TestEventURLModel(TestCase):

    def tearDown(self):
        for model in [models.EventURL, models.Event, User]:
            model.objects.all().delete()

    def test_event_url_is_created_successfully(self):
        user = get_user('us-ignite')
        event = fixtures.get_event(user=user)
        data = {
            'event': event,
            'name': 'US Ignite',
            'url': 'http://us-ignite.org/',
        }
        instance = models.EventURL.objects.create(**data)
        ok_(instance.id)
        eq_(instance.event, event)
        eq_(instance.name, 'US Ignite')
        eq_(instance.url, 'http://us-ignite.org/')


class TestEventTypeModel(TestCase):

    def test_audience_is_created_successfully(self):
        data = {'name': 'Networking'}
        instance = models.EventType.objects.create(**data)
        ok_(instance.id)
        eq_(instance.name, 'Networking')
        eq_(instance.slug, 'networking')

