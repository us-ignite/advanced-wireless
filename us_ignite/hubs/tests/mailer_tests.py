from mock import patch

from django.test import TestCase


from us_ignite.hubs import mailer


class TestNotifyRequest(TestCase):

    @patch('django.core.mail.mail_admins')
    def test_notification_is_sent_successfully(self, mock_mail):
        hub_request = object()
        mailer.notify_request(hub_request)
        mock_mail.assert_called_once()
