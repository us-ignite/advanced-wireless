from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase

from nose.tools import eq_, ok_
from mock import Mock

from us_ignite.profiles import communications


def _get_user_mock(email):
    user = Mock(spec=User)
    user.email = email
    return user


class TestSendWelcomeEmail(TestCase):

    def test_send_welcome_email_is_sent(self):
        user = _get_user_mock('someone@us-ignite.org')
        communications.send_welcome_email(user)
        eq_(len(mail.outbox), 1)
        eq_(mail.outbox[0].to, ['someone@us-ignite.org'])
