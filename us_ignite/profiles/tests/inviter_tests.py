import unittest

from nose.tools import ok_, eq_, raises
from mock import patch, MagicMock

from django import db
from django.core import mail
from django.contrib.auth.models import User
from django.test import TestCase

from django_browserid import auth
from us_ignite.profiles import inviter


class TestRawUser(TestCase):

    def test_inviter_can_be_instantiated_with_args(self):
        user = inviter.RawUser('John Donne', 'no-reply@us-ignite.org')
        eq_(user.name, 'John Donne')
        eq_(user.email, 'no-reply@us-ignite.org')

    def test_inviter_can_be_instantiated_with_kwargs(self):
        user = inviter.RawUser(
            name='John Donne', email='no-reply@us-ignite.org')
        eq_(user.name, 'John Donne')
        eq_(user.email, 'no-reply@us-ignite.org')

create_user = 'django.contrib.auth.models.User.objects.create_user'
get_user = 'django.contrib.auth.models.User.objects.get'


class TestCreateBrowserIDUser(TestCase):

    @patch(create_user)
    def test_create_user_succeeds(self, create_mock):
        email = 'no-reply@us-ignite.org'
        username = auth.default_username_algo(email)
        inviter.create_browserid_user(email)
        create_mock.assert_called_once_with(username, email)

    @patch(get_user)
    @patch(create_user, side_effect=db.IntegrityError)
    def test_create_user_fails_and_returns(self, create_mock, get_mock):
        email = 'other@us-ignite.org'
        username = auth.default_username_algo(email)
        inviter.create_browserid_user(email)
        create_mock.assert_called_once_with(username, email)
        get_mock.assert_called_once_with(email=email)


profile_get_or_create = 'us_ignite.profiles.models.Profile.objects.get_or_create'


def _get_or_create():
    return MagicMock(), True


class TestCreateUser(TestCase):

    @patch(get_user)
    def test_user_is_found_returns_none(self, get_mock):
        user = inviter.RawUser('Someone', 'someone@us-ignite.org')
        result = inviter.create_user(user)
        eq_(result, None)
        get_mock.assert_called_once()

    @patch(profile_get_or_create, return_value=_get_or_create())
    @patch('us_ignite.profiles.inviter.create_browserid_user', return_value=1)
    @patch(get_user, side_effect=User.DoesNotExist)
    def test_user_is_created(self, get_mock, create_mock, profile_mock):
        email = 'someone@us-ignite.org'
        user = inviter.RawUser('Someone', email)
        result = inviter.create_user(user)
        eq_(result, 1)
        get_mock.assert_called_once_with(email=email)
        create_mock.assert_called_once_with(email)
        profile_mock.assert_called_once_with(user=1)


class TestSednUserInvitation(TestCase):

    def test_invitation_is_successful(self):
        user = inviter.RawUser('John Donne', 'someone@us-ignite.org')
        inviter.send_user_invitation(user)
        eq_(len(mail.outbox), 1)
        eq_(mail.outbox[0].to, ['someone@us-ignite.org'])

    @unittest.skip
    def test_invitation_contains_link(self):
        user = inviter.RawUser('John Donne', 'someone@us-ignite.org')
        inviter.send_user_invitation(user)
        eq_(len(mail.outbox), 1)
        ok_(mail.outbox[0].body)


class TestInviteUsers(TestCase):

    @raises(TypeError)
    def test_invalid_list_raises_error(self):
        row_list = [('1', '2', '3')]
        inviter.invite_users(row_list)

    @patch('us_ignite.profiles.inviter.send_user_invitation')
    @patch('us_ignite.profiles.inviter.create_user', return_value=None)
    def test_existing_users_return_none(self, create_mock, mail_mock):
        row_list = [('John', 'no-reply@us-ignite.org')]
        result = inviter.invite_users(row_list)
        eq_(result, [])
        create_mock.assert_called_once()
        eq_(mail_mock.call_count, 0)

    @patch('us_ignite.profiles.inviter.send_user_invitation')
    @patch('us_ignite.profiles.inviter.create_user', return_value=7)
    def test_new_users_are_invited(self, create_mock, mail_mock):
        row_list = [('John', 'no-reply@us-ignite.org')]
        result = inviter.invite_users(row_list)
        eq_(result, [7])
        create_mock.assert_called_once()
        mail_mock.assert_called_once()
