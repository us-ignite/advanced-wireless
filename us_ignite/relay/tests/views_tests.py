from mock import patch, Mock
from nose.tools import assert_raises, eq_, ok_

from django.conf import settings
from django.http import Http404
from django.test import TestCase

from us_ignite.common.tests import utils
from us_ignite.relay import views
from us_ignite.profiles.models import Profile


patch_get = patch('us_ignite.relay.views.get_object_or_404')


class TestContactUserView(TestCase):

    def test_contact_user_requires_login(self):
        request = utils.get_request(
            'get', '/contact/foo/', user=utils.get_anon_mock())
        response = views.contact_user(request, 'foo')
        eq_(response.status_code, 302)
        eq_(response['Location'], utils.get_login_url('/contact/foo/'))

    @patch_get
    def test_invalid_profile_raises_404(self, mock_get):
        mock_get.side_effect = Http404
        request = utils.get_request(
            'get', '/contact/foo/', user=utils.get_user_mock())
        assert_raises(Http404, views.contact_user, request, 'foo')
        mock_get.assert_called_once()

    @patch_get
    def test_get_request_is_valid(self, mock_get):
        mock_profile = Mock(spec=Profile)()
        mock_get.return_value = mock_profile
        request = utils.get_request(
            'get', '/contact/foo/', user=utils.get_user_mock())
        response = views.contact_user(request, 'foo')
        eq_(response.status_code, 200)
        eq_(response.template_name, 'relay/contact_user.html')
        eq_(sorted(response.context_data), ['form', 'object'])

    @patch_get
    def test_empty_post_request_fails(self, mock_get):
        mock_profile = Mock(spec=Profile)()
        mock_get.return_value = mock_profile
        request = utils.get_request(
            'post', '/contact/foo/', data={}, user=utils.get_user_mock())
        response = views.contact_user(request, 'foo')
        ok_(response.context_data['form'].errors)

    @patch_get
    @patch('us_ignite.relay.engine.contact_user')
    def test_valid_post_request_succeeds(self, mock_contact, mock_get):
        mock_profile = Mock(spec=Profile)()
        mock_profile.get_absolute_url.return_value = '/accounts/user-slug/'
        mock_profile.display_email = 'info@us_ignite.org'
        mock_get.return_value = mock_profile
        data = {
            'title': 'Hi there!',
            'body': 'The app is quite interesting',
        }
        request = utils.get_request(
            'post', '/contact/foo/', data=data, user=utils.get_user_mock())
        request.user.email = 'user@us-ignite.org'
        request._messages = utils.TestMessagesBackend(request)
        response = views.contact_user(request, 'foo')
        eq_(response.status_code, 302)
        eq_(response['Location'], '/accounts/user-slug/')
        mock_contact.assert_called_once()
