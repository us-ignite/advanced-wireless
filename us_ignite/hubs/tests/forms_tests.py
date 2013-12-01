from nose.tools import eq_

from django.test import TestCase

from us_ignite.hubs import forms


class TestHubRequestForm(TestCase):

    def test_form_fields_are_not_sensitive(self):
        form = forms.HubRequestForm()
        eq_(sorted(form.fields.keys()),
            sorted(['name', 'website', 'summary', 'description']))

    def test_empty_form_fails(self):
        form = forms.HubRequestForm({})
        eq_(form.is_valid(), False)

    def test_valid_data_is_successful(self):
        data = {
            'name': 'Gigabit community',
            'description': 'Community description.',
        }
        form = forms.HubRequestForm(data)
        eq_(form.is_valid(), True)


class TestHubForm(TestCase):

    def test_form_fields_are_not_sensitive(self):
        form = forms.HubForm()
        eq_(sorted(form.fields.keys()),
            sorted(['name', 'website', 'summary', 'description', 'image',
                    'features', 'tags']))

    def test_empty_form_fails(self):
        form = forms.HubForm({})
        eq_(form.is_valid(), False)

    def test_valid_data_is_successful(self):
        data = {
            'name': 'Gigabit community',
            'description': 'Community description.',
        }
        form = forms.HubForm(data)
        eq_(form.is_valid(), True)


class TestHubAppMembershipForm(TestCase):

    def test_form_fields_are_not_sensitive(self):
        form = forms.HubAppMembershipForm()
        eq_(sorted(form.fields.keys()), ['hubs'])

    def test_empty_form_payload_succeeds(self):
        form = forms.HubAppMembershipForm({})
        eq_(form.is_valid(), True)


class TestHubApprovalRequestForm(TestCase):

    def test_form_fields_are_not_sensitive(self):
        form = forms.HubApprovalRequestForm()
        eq_(sorted(form.fields.keys()), ['notes', 'status'])

    def test_empty_form_payload_fails(self):
        form = forms.HubApprovalRequestForm({})
        eq_(form.is_valid(), False)

    def test_valid_form_payload_succeeds(self):
        form = forms.HubApprovalRequestForm({'status': 1})
        eq_(form.is_valid(), True)
