from mock import patch
from nose.tools import eq_, ok_

from django.test import client, TestCase

from us_ignite.common.tests import utils
from us_ignite.profiles import views


patch_app_filter = patch('us_ignite.apps.models.Application.objects.filter')


class TestUserProfileDeleteView(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def test_get_request_profile_requres_authentication(self):
        request = self.factory.get('/profile/delete/')
        request.user = utils.get_anon_mock()
        response = views.user_profile_delete(request)
        eq_(response.status_code, 302)
        eq_(response['Location'], utils.get_login_url('/profile/delete/'))

    def test_post_request_profile_requres_authentication(self):
        request = self.factory.post('/profile/delete/')
        request.user = utils.get_anon_mock()
        response = views.user_profile_delete(request)
        eq_(response.status_code, 302)
        eq_(response['Location'], utils.get_login_url('/profile/delete/'))

    @patch_app_filter
    def test_get_request_is_successful(self, app_mock):
        request = self.factory.get('/profile/delete/')
        request.user = utils.get_user_mock()
        response = views.user_profile_delete(request)
        app_mock.assert_called_once_with(owner=request.user)
        eq_(response.template_name, 'profile/user_profile_delete.html')
        eq_(sorted(response.context_data.keys()),
            sorted(['application_list', 'event_list', 'resource_list']))

    @patch_app_filter
    @patch('us_ignite.profiles.views.logout')
    def test_removal_request_is_successful(self, logout_mock, app_mock):
        app_mock.return_value = []
        request = self.factory.post('/profile/delete/')
        request.user = utils.get_user_mock()
        request._messages = utils.TestMessagesBackend(request)
        response = views.user_profile_delete(request)
        app_mock.assert_called_once_with(owner=request.user)
        request.user.delete.assert_called_once()
        logout_mock.assert_called_once_with(request)
        eq_(response.status_code, 302)
        eq_(response['Location'], '/')
