from nose.tools import eq_, ok_

from django.test import TestCase

from us_ignite.mailinglist import forms


class TestEmailForm(TestCase):

    def test_form_fiels_are_not_sensitive(self):
        form = forms.EmailForm()
        eq_(sorted(form.fields.keys()), ['email'])

    def test_form_requires_a_valid_email_address(self):
        form = forms.EmailForm({'email': 'foo'})
        eq_(form.is_valid(), False)
        ok_('email' in form.errors)

    def test_valid_payload_is_successful(self):
        form = forms.EmailForm({'email': 'user@us-ignite.org'})
        eq_(form.is_valid(), True)
