from mock import Mock
from nose.tools import eq_

from django.test import TestCase

from us_ignite.challenges import forms
from us_ignite.challenges.models import Challenge, Entry, EntryAnswer, Question


class TestGetEntryChoices(TestCase):

    def test_get_entry_choices_are_not_sensitive(self):
        choices = forms.get_entry_choices()
        eq_([i[0] for i in choices], [Entry.DRAFT, Entry.SUBMITTED])


class TestGetFieldName(TestCase):

    def test_field_name_is_valid(self):
        field_name = forms.get_field_name(3)
        eq_(field_name, 'question_3')


class TestGetChallengeForm(TestCase):

    def test_get_challenge_form(self):
        question_mock = Mock(spec=Question)()
        question_mock.id = 3
        question_mock.question = 'Question 3'
        question_mock.is_required = False
        challenge_mock = Mock(spec=Challenge)()
        challenge_mock.question_set.all.return_value = [question_mock]
        FormClass = forms.get_challenge_form(challenge_mock)
        form = FormClass()
        eq_(sorted(form.fields.keys()), ['question_3', 'status'])
        challenge_mock.question_set.all.assert_called_once()


class TestGetChallengeInitialData(TestCase):

    def test_data_is_extracted_successfully(self):
        answer_mock = Mock(spec=EntryAnswer)()
        answer_mock.question_id = 4
        answer_mock.answer = 'This will help society.'
        entry_mock = Mock(spec=Entry)()
        entry_mock.status = Entry.DRAFT
        entry_mock.entryanswer_set.all.return_value = [answer_mock]
        initial_data = forms.get_challenge_initial_data(entry_mock)
        eq_(initial_data, {
            'status': Entry.DRAFT,
            'question_4': 'This will help society.',
        })
