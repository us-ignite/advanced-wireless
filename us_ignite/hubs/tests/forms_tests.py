from nose.tools import eq_

from django.test import TestCase

from us_ignite.hubs import forms


class TestHubForm(TestCase):

    def test_form_fields_are_not_sensitive(self):
        form = forms.HubForm()
        eq_(sorted(form.fields.keys()),
            sorted(['name', 'website', 'summary', 'description']))

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
