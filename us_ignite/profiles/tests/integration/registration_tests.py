from unittest import skip

from django.contrib.auth.models import User
from django.core import mail
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.test import TestCase
from django.utils.http import int_to_base36


from django_nose.tools import assert_redirects
from registration.models import RegistrationProfile
from nose.tools import ok_, eq_

from us_ignite.common.tests import utils
from us_ignite.profiles.tests import fixtures


def _teardown_profiles():
    for model in [RegistrationProfile, User]:
        model.objects.all().delete()


class TestRegistrationForm(TestCase):

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
        _teardown_profiles()

    def test_successful_registration_sends_email(self):
        response = self.client.post('/accounts/register/', {
            'email': 'user-b@us-ignite.org',
            'password1': 'hello!',
            'password2': 'hello!',
        })
        ok_(len(mail.outbox), 1)
        key = response.context['activation_key']
        url = '%s%s' % (settings.SITE_URL,
                        reverse('registration_activate', args=[key]))
        ok_(url in mail.outbox[0].body)
        _teardown_profiles()


class TestActivationCompletePage(TestCase):

    def test_page_returns_valid_response(self):
        response = self.client.get('/accounts/activate/complete/')
        eq_(response.status_code, 200)


class TestActivationFailedPage(TestCase):

    def test_page_returns_valid_response(self):
        url = '/accounts/activate/1234567890123456789012345678901234567890/'
        response = self.client.get(url)
        eq_(response.status_code, 200)


class TestRegistrationCompletePage(TestCase):

    def test_page_returns_valid_response(self):
        url = '/accounts/register/complete/'
        response = self.client.get(url)
        eq_(response.status_code, 200)


class TestRegistrationClosedPage(TestCase):

    def test_page_returns_valid_response(self):
        url = '/accounts/register/closed/'
        response = self.client.get(url)
        eq_(response.status_code, 200)


class TestLoginFormPage(TestCase):

    def test_page_returns_valid_response(self):
        url = '/accounts/login/'
        response = self.client.get(url)
        eq_(response.status_code, 200)
        ok_(response.context['form'])

    # Requires the profile page to be created.
    @skip
    def test_login_page_succeeds(self):
        fixtures.get_user('hello', email='hello@us-ignite.org')
        payload  = {
            'username': 'hello@us-ignite.org',
            'password': 'hello',
        }
        response = self.client.post('/accounts/login/', payload)
        assert_redirects(response, '/accounts/profile/')


class TestLogoutPage(TestCase):

    def test_page_returns_valid_response(self):
        url = '/accounts/logout/'
        response = self.client.get(url)
        eq_(response.status_code, 200)


class TestUnauthenticatedPasswordChangePage(TestCase):

    def test_get_request_requires_authentication(self):
        url = '/accounts/password/change/'
        response = self.client.get(url)
        assert_redirects(response, utils.get_login_url(url))

    def test_post_request_requires_authentication(self):
        url = '/accounts/password/change/'
        payload = {
            'old_password': 'hello',
            'new_password1': 'hello123',
            'new_password2': 'hell0123',
        }
        response = self.client.post(url, payload)
        assert_redirects(response, utils.get_login_url(url))


class TestAuthenticatedPasswordChangePage(TestCase):

    def setUp(self):
        fixtures.get_user('hello')
        self.client.login(username='hello', password='hello')

    def tearDown(self):
        self.client.logout()
        _teardown_profiles()

    def test_get_request_succeds(self):
        url = '/accounts/password/change/'
        response = self.client.get(url)
        eq_(response.status_code, 200)
        ok_(response.context['form'])

    def test_post_request_succeds(self):
        url = '/accounts/password/change/'
        payload = {
            'old_password': 'hello',
            'new_password1': 'hello123',
            'new_password2': 'hello123',
        }
        response = self.client.post(url, payload)
        assert_redirects(response, reverse('auth_password_change_done'))

    def test_invalid_payload_fails(self):
        url = '/accounts/password/change/'
        payload = {
            'old_password': 'hello',
            'new_password1': 'bye123',
            'new_password2': 'hello123',
        }
        response = self.client.post(url, payload)
        eq_(response.status_code, 200)
        ok_(response.context['form'].errors)


class TestPasswordChangeDonePage(TestCase):

    def test_page_requires_authentication(self):
        url = '/accounts/password/change/done/'
        response = self.client.get(url)
        assert_redirects(response, utils.get_login_url(url))

    def test_authenticated_request_is_successful(self):
        fixtures.get_user('hello')
        self.client.login(username='hello', password='hello')
        url = '/accounts/password/change/done/'
        response = self.client.get(url)
        eq_(response.status_code, 200)
        _teardown_profiles()


class TestPasswordResetPage(TestCase):

    def test_page_returns_valid_response(self):
        url = '/accounts/password/reset/'
        response = self.client.get(url)
        eq_(response.status_code, 200)
        ok_(response.context['form'])

    def test_unregisted_email_POST_request_fails(self):
        payload = {
            'email': 'unregister@us-ignite.org',
        }
        response = self.client.post('/accounts/password/reset/', payload)
        eq_(response.status_code, 200)
        ok_(response.context['form'].errors)

    def test_valid_request_succeeds(self):
        fixtures.get_user('hello', email='hello@us-ignite.org')
        payload = {
            'email': 'hello@us-ignite.org',
        }
        response = self.client.post('/accounts/password/reset/', payload)
        assert_redirects(response, reverse('auth_password_reset_done'))
        eq_(len(mail.outbox), 1)
        expected_url = '%s/accounts/password/reset/confirm/' % settings.SITE_URL
        ok_(expected_url in mail.outbox[0].body)


class TestInvalidPasswordResetConfirmPage(TestCase):

    def test_invalid_token_returns_failed_response(self):
        url = '/accounts/password/reset/confirm/5-3lt-e42a9f141e6a1d649399/'
        response = self.client.get(url)
        eq_(response.status_code, 200)
        ok_('unsuccessful' in response.content.lower())

    def test_invalid_token_POST_request_fails(self):
        url = '/accounts/password/reset/confirm/5-3lt-e42a9f141e6a1d649399/'
        payload = {
            'new_password1': 'hello',
            'new_password2': 'hello',
        }
        response = self.client.post(url, payload)
        eq_(response.status_code, 200)
        ok_('unsuccessful' in response.content.lower())


class TestValidPasswordResetConfirmPage(TestCase):

    def setUp(self):
        user = fixtures.get_user('hello', email='hello@us-ignite.org')
        uid = int_to_base36(user.pk)
        token = default_token_generator.make_token(user)
        self._url = reverse('auth_password_reset_confirm',
                            kwargs={'uidb36': uid, 'token':token})

    def tearDown(self):
        _teardown_profiles()

    def test_GET_request_returns_valid_response(self):
        response = self.client.get(self._url)
        eq_(response.status_code, 200)
        ok_(response.context['form'])

    def test_valid_POST_request_is_successful(self):
        payload = {
            'new_password1': 'hello',
            'new_password2': 'hello',
        }
        response = self.client.post(self._url, payload)
        assert_redirects(response, reverse('auth_password_reset_complete'))


class TestResetCompletePage(TestCase):

    def test_page_returns_valid_response(self):
        url = '/accounts/password/reset/complete/'
        response = self.client.get(url)
        eq_(response.status_code, 200)


class TestResetDonepage(TestCase):

    def test_page_returns_valid_response(self):
        url = '/accounts/password/reset/done/'
        response = self.client.get(url)
        eq_(response.status_code, 200)
