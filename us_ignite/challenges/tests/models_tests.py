from dateutil.relativedelta import relativedelta
from nose.tools import eq_, ok_

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from us_ignite.apps.tests.fixtures import get_application
from us_ignite.challenges.models import Challenge, Entry, Question
from us_ignite.challenges.tests import fixtures
from us_ignite.profiles.tests.fixtures import get_user



class TestChallengeModel(TestCase):

    def tearDown(self):
        for model in [Challenge, User]:
            model.objects.all().delete()

    def test_instance_is_created_successfully(self):
        start_date = timezone.now()
        end_date = start_date + relativedelta(days=10)
        user = get_user('us-ignite')
        data = {
            'name': 'Gigabit challenge',
            'start_datetime': start_date,
            'end_datetime': end_date,
            'summary': 'Summary',
            'description': 'Description',
            'user': user,
        }
        instance = Challenge.objects.create(**data)
        ok_(instance.id)
        eq_(instance.name, 'Gigabit challenge')
        eq_(instance.slug, 'gigabit-challenge')
        eq_(instance.status, Challenge.DRAFT)
        eq_(instance.start_datetime, start_date)
        eq_(instance.end_datetime, end_date)
        eq_(instance.summary, 'Summary')
        eq_(instance.description,  'Description')
        eq_(instance.image, '')
        eq_(instance.organization, None)
        eq_(instance.user, user)
        eq_(instance.notes, '')
        ok_(instance.created)
        ok_(instance.modified)


class TestQuestionModel(TestCase):

    def tearDown(self):
        for model in [Question, Challenge, User]:
            model.objects.all().delete()

    def test_instance_is_created_successfully(self):
        user = get_user('us-ignite')
        challenge = fixtures.get_challenge(user=user)
        data = {
            'challenge': challenge,
            'question': 'How does your application improves society?',
        }
        instance = Question.objects.create(**data)
        ok_(instance.id)
        eq_(instance.challenge, challenge)
        eq_(instance.question, 'How does your application improves society?')
        eq_(instance.is_required, True)
        eq_(instance.order, 0)
        ok_(instance.created)
        ok_(instance.modified)


class TestEntryModel(TestCase):

    def tearDown(self):
        for model in [Entry, Challenge, User]:
            model.objects.all().delete()

    def test_instance_is_created_successfully(self):
        user = get_user('us-ignite')
        challenge = fixtures.get_challenge(user=user)
        application = get_application(owner=user)
        data = {
            'challenge': challenge,
            'application': application,
        }
        instance = Entry.objects.create(**data)
        ok_(instance.id)
        eq_(instance.challenge, challenge)
        eq_(instance.application, application)
        eq_(instance.status, Entry.PENDING)
        eq_(instance.notes, '')
        ok_(instance.created)
        ok_(instance.modified)
