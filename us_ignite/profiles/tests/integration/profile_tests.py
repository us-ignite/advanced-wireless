from django.test import TestCase
from django.contrib.auth.models import User

from django_nose.tools import assert_redirects
from registration.models import RegistrationProfile
from nose.tools import eq_

from us_ignite.common.tests import utils
from us_ignite.profiles.tests import fixtures


def _teardown_profiles():
    for model in [RegistrationProfile, User]:
        model.objects.all().delete()


class TestUnauthenticatedEditProfilePage(TestCase):

    def test_profile_requires_authentication(self):
        url = '/accounts/profile/'
        response = self.client.get(url)
        assert_redirects(response, utils.get_login_url(url))

    def test_profile_update_requires_authentication(self):
        url = '/accounts/profile/'
        data = {
            'first_name': 'John',
            'last_name': 'Donne',
        }
        response = self.client.post(url, data)
        assert_redirects(response, utils.get_login_url(url))


class TestEditProfilePage(TestCase):

    def setUp(self):
        fixtures.get_user('us-ignite', email='user@us-ignite.org')
        self.client.login(username='us-ignite', password='us-ignite')

    def tearDown(self):
        self.client.logout()
        _teardown_profiles()

    def test_profile_form_request_is_successful(self):
        url = '/accounts/profile/'
        response = self.client.get(url)
        fields = response.context['form'].fields.keys()
        eq_(sorted(fields), ['bio', 'first_name', 'last_name', 'website'])

    def test_profile_form_update_is_successful(self):
        url = '/accounts/profile/'
        data = {
            'first_name': 'John',
            'last_name': 'Donne',
        }
        response = self.client.post(url, data)
        assert_redirects(response, '/accounts/profile/')
        values = (User.objects.values('first_name', 'last_name')
                  .get(username='us-ignite'))
        eq_(values, data)

    def test_profile_ignores_invaid_values(self):
        url = '/accounts/profile/'
        data = {
            'email': 'invalid@us-ignite.org',
        }
        response = self.client.post(url, data)
        assert_redirects(response, '/accounts/profile/')
        values = (User.objects.values('email')
                  .get(username='us-ignite'))
        eq_(values, {'email': 'user@us-ignite.org'})
