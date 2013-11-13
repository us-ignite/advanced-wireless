from mock import patch, Mock
from nose.tools import eq_, ok_

from django.contrib.auth.models import User
from django.test import client, TestCase

from us_ignite.common.tests import utils
from us_ignite.profiles import views


def _get_anon_mock():
    """Generate an anon user mock."""
    user = Mock(spec=User)
    user.is_authenticated.return_value = False
    return user


def _get_user_mock():
    """Generate an authed user mock."""
    user = Mock(spec=User)
    user.is_authenticated.return_value = True
    return user


patch_app_filter = patch('us_ignite.apps.models.Application.objects.filter')


class TestUserProfileDeleteView(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def test_get_request_profile_requres_authentication(self):
        request = self.factory.get('/profile/delete/')
        request.user = _get_anon_mock()
        response = views.user_profile_delete(request)
        eq_(response.status_code, 302)
        eq_(response['Location'], utils.get_login_url('/profile/delete/'))

    def test_post_request_profile_requres_authentication(self):
        request = self.factory.post('/profile/delete/')
        request.user = _get_anon_mock()
        response = views.user_profile_delete(request)
        eq_(response.status_code, 302)
        eq_(response['Location'], utils.get_login_url('/profile/delete/'))

    @patch_app_filter
    def test_get_request_is_successful(self, app_mock):
        request = self.factory.get('/profile/delete/')
        request.user = _get_user_mock()
        response = views.user_profile_delete(request)
        app_mock.assert_called_once_with(owner=request.user)
        eq_(response.template_name, 'profile/user_profile_delete.html')
        ok_('application_list' in response.context_data)

    @patch_app_filter
    @patch('us_ignite.profiles.views.logout')
    def test_removal_request_is_successful(self, logout_mock, app_mock):
        app_mock.return_value = []
        request = self.factory.post('/profile/delete/')
        request.user = _get_user_mock()
        request._messages = utils.TestMessagesBackend(request)
        response = views.user_profile_delete(request)
        app_mock.assert_called_once_with(owner=request.user)
        request.user.delete.assert_called_once()
        logout_mock.assert_called_once_with(request)
        eq_(response.status_code, 302)
        eq_(response['Location'], '/')
