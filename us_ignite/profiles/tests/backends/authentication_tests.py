from django.contrib.auth.models import User
from django.test import TestCase

from mock import patch
from nose.tools import eq_,  ok_

from us_ignite.profiles.backends import authentication


user_does_not_exist = patch('django.contrib.auth.models.User.objects.get',
                            side_effect=User.DoesNotExist)


class TestEmaiModelBackend(TestCase):

    @patch('django.contrib.auth.models.User.objects.get')
    def test_valid_authentication_returns_user(self, get_user_mock):
        instance = get_user_mock()
        instance.check_password.return_value = True
        backend = authentication.EmailModelBackend()
        user = backend.authenticate('foo', 'bar')
        eq_(user, instance)

    @patch('django.contrib.auth.models.User.objects.get')
    def test_invalid_authentication_returns_none(self, get_user_mock):
        instance = get_user_mock()
        instance.check_password.return_value = False
        backend = authentication.EmailModelBackend()
        user = backend.authenticate('other', 'user')
        eq_(user, None)

    @user_does_not_exist
    def test_non_existing_user_returns_none(self, get_user_mock):
        backend = authentication.EmailModelBackend()
        user = backend.authenticate('foo', 'failed')
        eq_(user, None)
        get_user_mock.assert_called_once_with(email__iexact='foo')
