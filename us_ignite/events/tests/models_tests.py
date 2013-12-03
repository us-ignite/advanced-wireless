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
        data = {
            'name': 'Gigabit community meet-up',
            'venue': 'London, UK',
            'start_datetime': timezone.now(),
            'user': user,
        }
        instance = models.Event.objects.create(**data)
        ok_(instance.id)
        eq_(instance.name, 'Gigabit community meet-up'),
        ok_(instance.slug)
        eq_(instance.status, models.Event.DRAFT)
        eq_(instance.website, '')
        eq_(instance.image, '')
        eq_(instance.venue, 'London, UK')
        eq_(instance.description, '')
        eq_(list(instance.tags.all()), [])
        eq_(list(instance.hubs.all()), [])
        eq_(instance.user, user)
        eq_(instance.is_featured, False)
        eq_(instance.notes, '')
        ok_(instance.created)
        ok_(instance.modified)

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

