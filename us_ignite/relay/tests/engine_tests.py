from nose.tools import eq_, ok_

from django.core import mail
from django.test import TestCase

from us_ignite.relay import engine


class TestContactUser(TestCase):

    def test_contact_user(self):
        engine.contact_user('info@us-ignite.org', 'reply@us-ignite.org', {})
        eq_(len(mail.outbox), 1)
        email = mail.outbox[0]
        ok_(email.subject)
        ok_(email.body)
        ok_('Reply-To: reply@us-ignite.org\n' in unicode(email.message()))
        eq_(email.from_email, 'info@us-ignite.org')
