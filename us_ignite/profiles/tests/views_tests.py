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
