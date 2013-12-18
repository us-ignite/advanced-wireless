from mock import patch
from nose.tools import eq_, ok_

from django.contrib.auth.models import User
from django.test import TestCase

from us_ignite.apps.models import Application
from us_ignite.apps import forms
from us_ignite.common.tests import utils


class TestApplicationForm(TestCase):

    def test_fields_listed_are_not_sensitive(self):
        form = forms.ApplicationForm()
        expected_fields = sorted(
            ['name', 'summary', 'impact_statement', 'description',
             'image', 'domain',  'features', 'stage', 'roadmap',
             'assistance', 'team_description', 'acknowledgments',
             'tags', 'status'])
        eq_(sorted(form.fields.keys()), expected_fields)

    def test_removed_field_is_not_a_status_choice(self):
        form = forms.ApplicationForm()
        items = [k for k, v in form.fields['status'].choices]
        ok_(not Application.REMOVED in items)

    def test_initial_status_field_is_draft(self):
        form = forms.ApplicationForm()
        eq_(form.fields['status'].initial, Application.DRAFT)

    def test_form_minimum_values_are_valid(self):
        payload = {
            'name': 'Great Gigabit App',
            'description': 'This app will change everything.',
            'summary': 'This app is great!',
            'status': Application.DRAFT,
            'stage': Application.IDEA,
        }
        form = forms.ApplicationForm(payload)
        eq_(form.is_valid(), True)

    def test_form_cannot_set_status_to_removed(self):
        payload = {
            'name': 'Great Gigabit App',
            'description': 'This app will change everything.',
            'summary': 'This app is great!',
            'status': Application.REMOVED,
            'stage': Application.IDEA,
        }
        form = forms.ApplicationForm(payload)
        eq_(form.is_valid(), False)
        ok_('status' in form.errors)


patch_user_get = patch('django.contrib.auth.models.User.objects.get')


class TestMembershipForm(TestCase):

    def test_membership_form_does_not_contain_sensitive_information(self):
        form = forms.MembershipForm()
        eq_(sorted(form.fields), ['collaborators'])

    def test_empty_payload_succeeds(self):
        form = forms.MembershipForm({'collaborators': ''})
        eq_(form.is_valid(), True)
        eq_(form.cleaned_data['collaborators'], [])

    def test_invalid_emails_fails(self):
        form = forms.MembershipForm({'collaborators': 'INVALID'})
        eq_(form.is_valid(), False)
        ok_('invalid email' in unicode(form.errors['collaborators']))

    @patch_user_get
    def test_non_registered_member_fails(self, get_mock):
        get_mock.side_effect = User.DoesNotExist
        form = forms.MembershipForm({'collaborators': 'info@us-ignite.org'})
        eq_(form.is_valid(), False)
        ok_('not registered' in unicode(form.errors['collaborators']))

    @patch_user_get
    def test_registered_member_succeeds(self, get_mock):
        user_mock = utils.get_user_mock()
        get_mock.return_value = user_mock
        form = forms.MembershipForm({'collaborators': 'info@us-ignite.org'})
        eq_(form.is_valid(), True)
        eq_(form.cleaned_data['collaborators'], [user_mock])


class TestApplicationMembershipForm(TestCase):

    def test_form_does_not_list_sensitive_fields(self):
        form = forms.ApplicationMembershipForm()
        eq_(sorted(form.fields.keys()), ['can_edit', ])
