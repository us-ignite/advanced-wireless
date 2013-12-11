from dateutil.relativedelta import relativedelta
from nose.tools import eq_

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from us_ignite.apps.models import Application
from us_ignite.apps.tests.fixtures import get_application
from us_ignite.challenges.models import Challenge, Question, Entry
from us_ignite.challenges.tests import fixtures
from us_ignite.profiles.tests.fixtures import get_user


class TestActiveChallengesManager(TestCase):

    def tearDown(self):
        for model in [Challenge, User]:
            model.objects.all().delete()

    def test_active_chalenge_is_returned(self):
        user = get_user('us-ignite')
        start = timezone.now()
        end = start + relativedelta(days=2)
        data = {
            'user': user,
            'start_datetime': start,
            'end_datetime': end,
            'status': Challenge.PUBLISHED,
        }
        instance = fixtures.get_challenge(**data)
        eq_(list(Challenge.active.all()), [instance])

    def test_past_challenge_is_not_returned(self):
        user = get_user('us-ignite')
        start = timezone.now() - relativedelta(days=3)
        end = start + relativedelta(days=2)
        data = {
            'user': user,
            'start_datetime': start,
            'end_datetime': end,
            'status': Challenge.PUBLISHED,
        }
        fixtures.get_challenge(**data)
        eq_(list(Challenge.active.all()), [])

    def test_future_challenge_is_not_returned(self):
        user = get_user('us-ignite')
        start = timezone.now() + relativedelta(days=3)
        end = start + relativedelta(days=2)
        data = {
            'user': user,
            'start_datetime': start,
            'end_datetime': end,
            'status': Challenge.PUBLISHED,
        }
        fixtures.get_challenge(**data)
        eq_(list(Challenge.active.all()), [])

    def test_not_active_chalenge_is_not_returned(self):
        user = get_user('us-ignite')
        start = timezone.now()
        end = start + relativedelta(days=2)
        data = {
            'user': user,
            'start_datetime': start,
            'end_datetime': end,
            'status': Challenge.DRAFT,
        }
        fixtures.get_challenge(**data)
        eq_(list(Challenge.active.all()), [])


class TestQuestionManager(TestCase):

    def tearDown(self):
        for model in [Challenge, Question, User]:
            model.objects.all().delete()

    def test_questions_are_returned_from_keys(self):
        challenge = fixtures.get_challenge()
        question = fixtures.get_question(challenge, id=3)
        question_list = Question.objects.get_from_keys(['question_3'])
        eq_(list(question_list), [question])


class TestEntryManager(TestCase):

    def tearDown(self):
        for model in [Entry, Challenge, Application, User]:
            model.objects.all().delete()

    def test_missing_entry_returns_none(self):
        user = get_user('us-ignite')
        challenge = fixtures.get_challenge(user=user)
        application = get_application(owner=user)
        eq_(Entry.objects.get_entry_or_none(challenge, application), None)

    def test_existing_entry_is_returned(self):
        user = get_user('us-ignite')
        challenge = fixtures.get_challenge(user=user)
        application = get_application(owner=user)
        entry = fixtures.get_entry(
            application, challenge=challenge, status=Entry.SUBMITTED)
        eq_(Entry.objects.get_entry_or_none(challenge, application), entry)
