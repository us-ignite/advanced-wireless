from nose.tools import eq_, ok_

from django.contrib.auth.models import User
from django.test import TestCase

from us_ignite.events import models
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
            'user': user,
        }
        instance = models.Event.objects.create(**data)
        ok_(instance.id)
        eq_(instance.name, 'Gigabit community meet-up'),
        ok_(instance.slug)
        eq_(instance.status, models.Event.DRAFT)
        eq_(instance.website, '')
        eq_(instance.venue, 'London, UK')
        eq_(instance.description, '')
        eq_(list(instance.tags.all()), [])
        eq_(instance.user, user)
        eq_(instance.is_featured, False)
        eq_(instance.notes, '')
        ok_(instance.created)
        ok_(instance.modified)
