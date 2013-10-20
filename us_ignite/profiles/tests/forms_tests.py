from nose.tools import ok_, eq_
from mock import patch

from django.test import TestCase
from django.contrib.auth.models import User

from us_ignite.profiles.forms import UserRegistrationForm, ProfileForm

user_get = 'django.contrib.auth.models.User.objects.get'


class TestUserRegistrationForm(TestCase):

    def test_default_fields(self):
        form = UserRegistrationForm()
        fields = form.fields.keys()
        eq_(sorted(fields), ['email', 'password1', 'password2'])

    def test_empty_form_fails(self):
        form = UserRegistrationForm({})
        eq_(form.is_valid(), False)
        ok_('email' in form.errors)
        ok_('password1' in form.errors)
        ok_('password2' in form.errors)

    def test_form_with_empty_fields_fails(self):
        form = UserRegistrationForm({
            'email': '',
            'password1': '',
            'password2': '',
        })
        eq_(form.is_valid(), False)
        ok_('email' in form.errors)
        ok_('password1' in form.errors)
        ok_('password2' in form.errors)

    def test_form_with_different_passwords_fails(self):
        form = UserRegistrationForm({
            'email': 'user@us-ignite.org',
            'password1': 'alpha',
            'password2': 'omega',
        })
        eq_(form.is_valid(), False)
        ok_(form.non_field_errors())

    @patch(user_get, return_value=User())
    def test_form_with_registered_email_fails(self, user_get_mock):
        form = UserRegistrationForm({
            'email': 'user-b@us-ignite.org',
            'password1': 'abc',
            'password2': 'abc',
        })
        eq_(form.is_valid(), False)
        ok_('email' in form.errors)
        user_get_mock.assert_called_once_with(email__iexact='user-b@us-ignite.org')

    @patch(user_get, side_effect=User.DoesNotExist)
    def test_form_succeeds_with_valid_values(self, user_get_mock):
        form = UserRegistrationForm({
            'email': 'user-c@us-ignite.org',
            'password1': 'abc',
            'password2': 'abc',
        })
        eq_(form.is_valid(), True)
        user_get_mock.assert_called_once_with(email__iexact='user-c@us-ignite.org')


class TestProfileForm(TestCase):

    def test_form_list_non_sensitive_values(self):
        form = ProfileForm()
        eq_(sorted(form.fields.keys()),
            ['bio', 'first_name', 'last_name', 'website'])

    def test_form_accepts_empty_payload(self):
        form = ProfileForm({})
        ok_(form.is_valid())

    def test_form_accepts_empty_values(self):
        form = ProfileForm({
            'first_name': '',
            'last_name': '',
            'bio': '',
            'website': '',
        })
        ok_(form.is_valid())

    def test_form_receives_valid_values(self):
        form = ProfileForm({
            'first_name': 'John',
            'last_name': 'Donne',
            'bio': 'English poet, satirist and lawyer.',
            'website': 'http://en.wikipedia.org/wiki/John_Donne',
        })
        ok_(form.is_valid())
