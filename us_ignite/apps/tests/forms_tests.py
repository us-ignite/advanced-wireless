from mock import patch, Mock
from nose.tools import eq_, ok_

from django.contrib.auth.models import User
from django.test import TestCase

from us_ignite.apps.models import Application
from us_ignite.apps import forms


class TestApplicationForm(TestCase):

    def test_fields_listed_are_not_sensitive(self):
        form = forms.ApplicationForm()
        eq_(sorted(form.fields.keys()),
            ['assistance', 'description', 'image', 'name',
             'short_description', 'stage', 'status', 'tags', 'technology'])

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
            'status': Application.DRAFT,
            'stage': Application.IDEA,
        }
        form = forms.ApplicationForm(payload)
        eq_(form.is_valid(), True)

    def test_form_cannot_set_status_to_removed(self):
        payload = {
            'name': 'Great Gigabit App',
            'description': 'This app will change everything.',
            'status': Application.REMOVED,
            'stage': Application.IDEA,
        }
        form = forms.ApplicationForm(payload)
        eq_(form.is_valid(), False)
        ok_('status' in form.errors)


patch_user_get = patch('django.contrib.auth.models.User.objects.get')


def _get_user_mock():
    """Generate an authed user mock."""
    user = Mock(spec=User)
    user.is_authenticated.return_value = True
    return user


class TestMembershipForm(TestCase):

    def test_membership_form_does_not_contain_sensitive_information(self):
        form = forms.MembershipForm()
        eq_(sorted(form.fields), ['collaborators'])

    def test_empty_payload_fails(self):
        form = forms.MembershipForm({'collaborators': ''})
        eq_(form.is_valid(), False)

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
        user_mock = _get_user_mock()
        get_mock.return_value = user_mock
        form = forms.MembershipForm({'collaborators': 'info@us-ignite.org'})
        eq_(form.is_valid(), True)
        eq_(form.cleaned_data['collaborators'], [user_mock])
