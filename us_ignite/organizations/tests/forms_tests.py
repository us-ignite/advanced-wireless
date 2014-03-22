from nose.tools import eq_

from django.test import TestCase

from us_ignite.organizations import forms


class TestOrganizationForm(TestCase):

    def test_fields_are_not_sensitive(self):
        form = forms.OrganizationForm()
        eq_(sorted(form.fields.keys()),
            sorted(['name', 'bio', 'image', 'website', 'interest_ignite',
                    'interests', 'interests_other', 'resources_available',
                    'tags', 'position']))

    def test_form_fails_with_empty_payload(self):
        form = forms.OrganizationForm({})
        eq_(form.is_valid(), False)

    def test_form_valid_payload(self):
        data = {
            'name': 'US Ignite',
            'bio': 'US Ignite',
        }
        form = forms.OrganizationForm(data)
        eq_(form.is_valid(), True)
