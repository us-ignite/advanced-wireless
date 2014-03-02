from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase

from nose.tools import eq_
from mock import Mock, patch

from us_ignite.profiles import communications


def _get_user_mock(email):
    user = Mock(spec=User)
    user.email = email
    return user


patch_snippet = patch('us_ignite.snippets.models.Snippet.published.get_from_key')

class TestSendWelcomeEmail(TestCase):

    @patch_snippet
    def test_send_welcome_email_is_sent(self, snippet_mock):
        user = _get_user_mock('someone@us-ignite.org')
        communications.send_welcome_email(user)
        eq_(len(mail.outbox), 1)
        eq_(mail.outbox[0].to, ['someone@us-ignite.org'])
        snippet_mock.assert_called_once_with('welcome-email')
