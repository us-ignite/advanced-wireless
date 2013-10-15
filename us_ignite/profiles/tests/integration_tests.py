from nose.tools import ok_, eq_

from django.contrib.auth.models import User
from django.test import TestCase

from django_nose.tools import assert_redirects
from registration.models import RegistrationProfile


def _remove_profiles():
    for model in [RegistrationProfile, User]:
        model.objects.all().delete()


class RegistrationForm(TestCase):

    def test_registration_page_exists(self):
        response = self.client.get('/accounts/register/')
        eq_(response.status_code, 200)

    def test_registration_page_contains_form(self):
        response = self.client.get('/accounts/register/')
        ok_('form' in response.context_data)

    def test_empty_registration_page_fails(self):
        response = self.client.post('/accounts/register/', {
            'email': '',
            'password1': '',
            'password2': '',
        })
        eq_(response.status_code, 200)
        ok_('errorlist' in response.content)

    def test_registration_is_successful(self):
        response = self.client.post('/accounts/register/', {
            'email': 'user@us-ignite.org',
            'password1': 'hello!',
            'password2': 'hello!',
        })
        assert_redirects(response, '/accounts/register/complete/')
        _remove_profiles()
