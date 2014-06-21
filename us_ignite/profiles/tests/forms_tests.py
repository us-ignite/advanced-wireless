from nose.tools import ok_, eq_, raises
from mock import patch

from django.forms import ValidationError
from django.test import TestCase
from django.contrib.auth.models import User

from us_ignite.profiles.forms import (
    InviterForm,
    ProfileForm,
    UserExportForm,
    UserRegistrationForm,
)
from us_ignite.profiles.models import Profile

user_get = 'django.contrib.auth.models.User.objects.get'


class TestUserRegistrationForm(TestCase):

    def test_default_fields(self):
        form = UserRegistrationForm()
        fields = form.fields.keys()
        eq_(sorted(fields),
            sorted(['first_name', 'last_name', 'email',
                    'password1', 'password2']))

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
        user_get_mock.assert_called_once_with(
            email__iexact='user-c@us-ignite.org')


class TestProfileForm(TestCase):

    def test_form_list_non_sensitive_values(self):
        form = ProfileForm()
        eq_(sorted(form.fields.keys()),
            sorted(['availability', 'bio', 'category', 'category_other',
                    'first_name', 'interests', 'interests_other',
                    'is_public', 'last_name', 'position', 'quote',
                    'skills', 'slug', 'tags', 'website']))

    def test_form_accepts_default_payload(self):
        form = ProfileForm({
            'availability': Profile.NO_AVAILABILITY,
            'first_name': 'someone',
            'slug': 'foo',
        })
        ok_(form.is_valid())

    def test_form_accepts_empty_values(self):
        form = ProfileForm({
            'name': '',
            'bio': '',
            'website': '',
            'availability': Profile.NO_AVAILABILITY,
            'first_name': 'someone',
            'slug': 'foo',
        })
        ok_(form.is_valid())

    def test_form_receives_valid_values(self):
        form = ProfileForm({
            'bio': 'English poet, satirist and lawyer.',
            'website': 'http://en.wikipedia.org/wiki/John_Donne',
            'availability': Profile.NO_AVAILABILITY,
            'first_name': 'someone',
            'slug': 'foo',
        })
        ok_(form.is_valid())


class TestInviterForm(TestCase):

    def test_form_fields_are_not_sensitive(self):
        form = InviterForm()
        eq_(sorted(form.fields.keys()), ['users', ])

    def test_form_with_invalid_format_fails(self):
        users = "Alpha, alpha@us-ignite.org, extra"
        form = InviterForm({'users': users})
        eq_(form.is_valid(), False)
        ok_('users' in form.errors)

    def test_form_with_invalid_email_fails(self):
        users = "Alpha, not an email."
        form = InviterForm({'users': users})
        eq_(form.is_valid(), False)
        ok_('users' in form.errors)

    def test_valid_submission_is_accepted(self):
        users = "Alpha, alpha@us-ignite.org"
        form = InviterForm({'users': users})
        eq_(form.is_valid(), True)
        eq_(form.cleaned_data['users'], [('Alpha', 'alpha@us-ignite.org')])

    def test_multiple_line_submission_is_accepted(self):
        users = ["Alpha, alpha@us-ignite.org", "Beta, beta@us-ignite.org"]
        users = '\n'.join(users)
        form = InviterForm({'users': users})
        eq_(form.is_valid(), True)
        eq_(form.cleaned_data['users'], [
            ('Alpha', 'alpha@us-ignite.org'),
            ('Beta', 'beta@us-ignite.org'),
        ])

    def test_blank_lines_are_ignored(self):
        users = [""] * 10
        users += ["Alpha,alpha@us-ignite.org"]
        users = '\n'.join(users)
        form = InviterForm({'users': users})
        eq_(form.is_valid(), True)
        eq_(form.cleaned_data['users'], [('Alpha', 'alpha@us-ignite.org')])

    @raises(ValidationError)
    def test_user_validation_fails_with_short_row(self):
        form = InviterForm()
        user_row = ('alpha',)
        form._validate_user(user_row)

    @raises(ValidationError)
    def test_user_validation_fails_with_long_row(self):
        form = InviterForm()
        user_row = ('alpha', 'beta', 'gamma')
        form._validate_user(user_row)

    @raises(ValidationError)
    def test_user_validation_fails_with_invalid_email(self):
        form = InviterForm()
        user_row = ('alpha', 'beta')
        form._validate_user(user_row)

    def test_user_validation_succeeds_with_valid_row(self):
        form = InviterForm()
        # Please note the whitespace at the begining of the email:
        user_row = ('alpha', ' beta@us-ignite.org')
        result = form._validate_user(user_row)
        eq_(result, ('alpha', 'beta@us-ignite.org'))


class TestUserExportForm(TestCase):

    def test_form_fileds_are_not_sensitive(self):
        form = UserExportForm()
        eq_(sorted(form.fields.keys()), ['end', 'start'])

    def test_form_is_valid_with_empty_values(self):
        form = UserExportForm({})
        eq_(form.is_valid(), True)

    def test_form_fails_when_start_date_is_in_the_future(self):
        data = {
            'start_0': '2013-12-6',
            'start_1': '00:00:00',
            'end_0': '2013-12-5',
            'end_1': '00:00:00',
        }
        form = UserExportForm(data)
        eq_(form.is_valid(), False)
        ok_(form.non_field_errors())

    def test_form_is_valid_with_start_date(self):
        data = {
            'start_0': '2013-12-6',
            'start_1': '00:00:00',
        }
        form = UserExportForm(data)
        eq_(form.is_valid(), True)

    def test_form_is_valid_with_end_date(self):
        data = {
            'end_0': '2013-12-6',
            'end_1': '00:00:00',
        }
        form = UserExportForm(data)
        eq_(form.is_valid(), True)
