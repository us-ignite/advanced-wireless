from nose.tools import eq_, ok_

from django.test import TestCase

from us_ignite.apps.models import Application
from us_ignite.apps import forms


class TestApplicationForm(TestCase):

    def test_fields_listed_are_not_sensitive(self):
        form = forms.ApplicationForm()
        eq_(sorted(form.fields.keys()),
            ['assistance','description', 'name', 'status', 'tags', 'technology',])

    def test_removed_field_is_not_a_status_choice(self):
        form = forms.ApplicationForm()
        items = [k for k, v in form.fields['status'].choices]
        ok_(not Application.REMOVED in items)

    def test_initial_status_field_is_draft(self):
        form = forms.ApplicationForm()
        eq_(form.fields['status'].initial, Application.DRAFT)

    def test_form_minimum_values_are_valid(self):
        payload = {
            'name': 'Great Gigabit App',
            'description': 'This app will change everything.',
            'status': Application.DRAFT,
        }
        form = forms.ApplicationForm(payload)
        eq_(form.is_valid(), True)

    def test_form_cannot_set_status_to_removed(self):
        payload = {
            'name': 'Great Gigabit App',
            'description': 'This app will change everything.',
            'status': Application.REMOVED,
        }
        form = forms.ApplicationForm(payload)
        eq_(form.is_valid(), False)
        ok_('status' in form.errors)

