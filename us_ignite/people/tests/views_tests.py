from mock import patch, Mock
from nose.tools import eq_, ok_, assert_raises

from django.contrib.auth.models import User
from django.http import Http404
from django.test import client, TestCase

from us_ignite.apps.models import Application
from us_ignite.common.tests import utils
from us_ignite.profiles.tests import fixtures
from us_ignite.people import views


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


def _teardown_profiles():
    for model in [User]:
        model.objects.all().delete()


class TestProfileListView(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def _get_request(self, url='/people/', data=None):
        data = data if data else {}
        request = self.factory.get(url, data)
        request.user = _get_user_mock()
        return request

    def test_profile_list_requires_authentication(self):
        request = self.factory.get('/people/')
        request.user = _get_anon_mock()
        response = views.profile_list(request)
        eq_(response.status_code, 302)
        eq_(response['Location'], utils.get_login_url('/people/'))

    def test_authenticated_profile_list_is_successful(self):
        request = self._get_request()
        response = views.profile_list(request)
        eq_(response.status_code, 200)
        eq_(len(response.context_data['page'].object_list), 0)

    def test_authenticated_profile_list_context(self):
        response = views.profile_list(self._get_request())
        eq_(response.status_code, 200)
        eq_(sorted(response.context_data.keys()),
            ['order', 'order_form', 'page'])

    def test_admin_users_are_not_listed(self):
        user = fixtures.get_user('us-ignite', is_superuser=True)
        fixtures.get_profile(user=user, name='us ignite')
        response = views.profile_list(self._get_request())
        eq_(response.status_code, 200)
        eq_(len(response.context_data['page'].object_list), 0)
        _teardown_profiles()

    def test_inactive_users_are_not_listed(self):
        user = fixtures.get_user('us-ignite', is_active=False)
        fixtures.get_profile(user=user, name='us ignite')
        response = views.profile_list(self._get_request())
        eq_(response.status_code, 200)
        eq_(len(response.context_data['page'].object_list), 0)
        _teardown_profiles()

    def test_users_can_be_sorted(self):
        user_a = fixtures.get_user('alpha')
        profile_a = fixtures.get_profile(user=user_a, name='alpha')
        user_b = fixtures.get_user('beta')
        profile_b = fixtures.get_profile(user=user_b, name='beta')
        request = self._get_request(data={'order': 'name'})
        response = views.profile_list(request)
        eq_(list(response.context_data['page'].object_list),
            [profile_a, profile_b])
        _teardown_profiles()

    def test_users_can_be_reverse_sorted(self):
        user_a = fixtures.get_user('alpha')
        profile_a = fixtures.get_profile(user=user_a, name='alpha')
        user_b = fixtures.get_user('beta')
        profile_b = fixtures.get_profile(user=user_b, name='beta')
        request = self._get_request(data={'order': '-name'})
        response = views.profile_list(request)
        eq_(list(response.context_data['page'].object_list),
            [profile_b, profile_a])
        _teardown_profiles()


class TestProfileDetailView(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def _get_request(self, url='/people/someone/', data=None):
        data = data if data else {}
        request = self.factory.get(url, data)
        request.user = _get_user_mock()
        return request

    def test_profile_detail_requires_authentication(self):
        request = self.factory.get('/people/someone/')
        request.user = _get_anon_mock()
        response = views.profile_detail(request)
        eq_(response.status_code, 302)
        eq_(response['Location'], utils.get_login_url('/people/someone/'))

    def test_superuser_profile_is_unavailable(self):
        user = fixtures.get_user('us-ignite', is_superuser=True)
        fixtures.get_profile(user=user, slug='someone', name='us ignite')
        request = self._get_request()
        assert_raises(Http404, views.profile_detail, request, 'someone')
        _teardown_profiles()

    def test_get_request_is_successful(self):
        user = fixtures.get_user('us-ignite')
        fixtures.get_profile(user=user, slug='someone', name='us ignite')
        response = views.profile_detail(self._get_request(), 'someone')
        ok_(response.status_code, 200)
        eq_(sorted(response.context_data.keys()), ['app_list', 'object'])
        _teardown_profiles()


app_active_filter = 'us_ignite.apps.models.Application.active.filter'


class TestGetUserAppsHelper(TestCase):

    def test_empty_viewer_returns_public_apps(self):
        owner = _get_user_mock()
        with patch(app_active_filter, return_value=[]) as filter_mock:
            result = views.get_user_apps(owner)
            eq_(result, [])
            filter_mock.assert_called_once_with(
                owner=owner, status=Application.PUBLISHED)

    def test_different_viewer_returns_public_apps(self):
        owner = _get_user_mock()
        viewer = _get_user_mock()
        with patch(app_active_filter, return_value=[]) as filter_mock:
            result = views.get_user_apps(owner, viewer=viewer)
            eq_(result, [])
            filter_mock.assert_called_once_with(
                owner=owner, status=Application.PUBLISHED)

    def test_owner_viewer_returns_all_apps(self):
        owner = _get_user_mock()
        with patch(app_active_filter, return_value=[]) as filter_mock:
            result = views.get_user_apps(owner, viewer=owner)
            eq_(result, [])
            filter_mock.assert_called_once_with(owner=owner)
