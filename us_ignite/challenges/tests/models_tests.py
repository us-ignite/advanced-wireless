from dateutil.relativedelta import relativedelta
from nose.tools import eq_, ok_

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from us_ignite.apps.models import Application
from us_ignite.apps.tests.fixtures import get_application
from us_ignite.challenges.models import Challenge, Entry, EntryAnswer, Question
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

    def test_instance_is_published(self):
        user = get_user('us-ignite')
        instance = fixtures.get_challenge(user=user, status=Challenge.PUBLISHED)
        eq_(instance.is_published(), True)

    def test_instance_is_draft(self):
        user = get_user('us-ignite')
        instance = fixtures.get_challenge(user=user, status=Challenge.DRAFT)
        eq_(instance.is_draft(), True)

    def test_instance_is_removed(self):
        user = get_user('us-ignite')
        instance = fixtures.get_challenge(user=user, status=Challenge.REMOVED)
        eq_(instance.is_removed(), True)


class TestQuestionModel(TestCase):

    def tearDown(self):
        for model in [Question, Challenge, Application, User]:
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
        for model in [Entry, Challenge, Application, User]:
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
        eq_(instance.status, Entry.DRAFT)
        eq_(instance.notes, '')
        ok_(instance.created)
        ok_(instance.modified)

    def test_instance_is_pending(self):
        user = get_user('us-ignite')
        challenge = fixtures.get_challenge(user=user)
        application = get_application(owner=user)
        entry = fixtures.get_entry(
            application, challenge=challenge, status=Entry.PENDING)
        eq_(entry.is_pending(), True)

    def test_instance_is_accepted(self):
        user = get_user('us-ignite')
        challenge = fixtures.get_challenge(user=user)
        application = get_application(owner=user)
        entry = fixtures.get_entry(
            application, challenge=challenge, status=Entry.ACCEPTED)
        eq_(entry.is_accepted(), True)

    def test_instance_is_rejected(self):
        user = get_user('us-ignite')
        challenge = fixtures.get_challenge(user=user)
        application = get_application(owner=user)
        entry = fixtures.get_entry(
            application, challenge=challenge, status=Entry.REJECTED)
        eq_(entry.is_rejected(), True)

    def test_instance_is_draft(self):
        user = get_user('us-ignite')
        challenge = fixtures.get_challenge(user=user)
        application = get_application(owner=user)
        entry = fixtures.get_entry(
            application, challenge=challenge, status=Entry.DRAFT)
        eq_(entry.is_draft(), True)


class TestEntryAnswerModel(TestCase):

    def tearDown(self):
        for model in [Question, Entry, Challenge, Application, User]:
            model.objects.all().delete()

    def test_entry_can_be_created_successfully(self):
        user = get_user('us-ignite')
        challenge = fixtures.get_challenge(user=user)
        application = get_application(owner=user)
        question = fixtures.get_question(challenge)
        entry = fixtures.get_entry(application)
        data = {
            'entry': entry,
            'question': question,
            'answer': 'Uses Gigabit features.'
        }
        instance = EntryAnswer.objects.create(**data)
        ok_(instance.id)
        eq_(instance.question, question)
        eq_(instance.answer, 'Uses Gigabit features.')
        ok_(instance.created)
        ok_(instance.modified)
