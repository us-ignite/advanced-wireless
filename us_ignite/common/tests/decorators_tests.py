from django.test import client, TestCase
from django.contrib.auth.models import Group, User

from mock import Mock, patch
from nose.tools import eq_, raises

from us_ignite.common import decorators
from us_ignite.common.tests import utils
from us_ignite.profiles.tests import fixtures


def dummy_view(request, response='ok'):
    return response


def _get_non_auth_user_mock():
    """Generate an unauthenticated ``User`` mock."""
    user = Mock(spec=User)
    user.is_authenticated.return_value = False
    return user


def _get_auth_user_mock():
    """Generate an authenticated ``User`` mock."""
    user = Mock(spec=User)
    user.is_authenticated.return_value = True
    return user


class TestGroupRequiredDecorator(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    @raises(TypeError)
    def test_decorator_missing_group_list_raises_exception(self):
        decorators.group_required()(dummy_view)

    def test_decorator_require_authenticated_user(self):
        request = self.factory.get('/custom-url/')
        request.user = _get_non_auth_user_mock()
        view = decorators.group_required(['foo'])(dummy_view)
        response = view(request)
        expected_url = utils.get_login_url('http%3A//testserver/custom-url/')
        eq_(response['Location'], expected_url)


class TestGroupRequiredDecoratorFixtured(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()
        self.user = fixtures.get_user('john')

    def tearDown(self):
        for model in [User, Group]:
            model.objects.all().delete()

    def test_user_not_in_group_fails(self):
        request = self.factory.get('/other-url/')
        request.user = self.user
        view = decorators.group_required(['foo'])(dummy_view)
        response = view(request)
        eq_(response.status_code, 200)
        eq_(response.template_name, 'unavailable.html')

    def test_user_group_succeeds(self):
        request = self.factory.get('/resource-url/')
        request.user = self.user
        group = Group.objects.create(name='special_resources')
        group.user_set.add(self.user)
        view = decorators.group_required('special_resources')(dummy_view)
        response = view(request, 'OK')
        eq_(response, 'OK')

    def test_user_multi_group_succeeds(self):
        request = self.factory.get('/asset-url/')
        request.user = self.user
        group = Group.objects.create(name='downloads')
        group.user_set.add(self.user)
        view = decorators.group_required(
            ['downloads', 'special_resources'])(dummy_view)
        response = view(request, 'OK')
        eq_(response, 'OK')


class TestNonAuthRequired(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def test_authenticated_user_is_redirected(self):
        request = self.factory.get('/alpha/')
        request.user = _get_auth_user_mock()
        view = decorators.not_auth_required(dummy_view)
        response = view(request, 'OK')
        eq_(response.status_code, 302)
        eq_(response['Location'], '/')

    def test_unauth_user_request_is_successful(self):
        request = self.factory.get('/beta/')
        request.user = _get_non_auth_user_mock()
        view = decorators.not_auth_required(dummy_view)
        response = view(request, 'OK1')
        eq_(response, 'OK1')


class ThottleDecoratorTest(TestCase):

    def setUp(self):
        # key is a mk5 key, determined between the remote ip and
        # path from the request
        self.key = '8243f83255259f10db07a5c781f7c3ab'
        self.factory = client.RequestFactory()
        kwargs = {'HTTP_X_FORWARDED_FOR': '127.0.0.1'}
        self.request = self.factory.get('/', **kwargs)
        self.request.user = utils.get_anon_mock()

    @patch('django.core.cache.cache.set', return_value=True)
    @patch('django.core.cache.cache.get', return_value=False)
    def test_view_not_in_cache(self, cache_get, cache_set):
        decorator = decorators.throttle_view(methods=['GET'], duration=30)
        mocked = decorator(dummy_view)
        response = mocked(self.request)
        cache_get.assert_called_with(self.key)
        cache_set.assert_called_with(self.key, True, 30)
        eq_(response, 'ok')

    @patch('django.core.cache.cache.set', return_value=True)
    @patch('django.core.cache.cache.get', return_value=True)
    def test_view_in_cache(self, cache_get, cache_set):
        decorator = decorators.throttle_view(methods=['GET'], duration=30)
        mocked = decorator(dummy_view)
        response = mocked(self.request)
        cache_get.assert_called_with(self.key)
        eq_(cache_set.called, False)
        eq_(response.status_code, 503)
        eq_(response['Retry-After'], '30')

    @patch('django.core.cache.cache.set', return_value=True)
    @patch('django.core.cache.cache.get', return_value=False)
    def test_other_method_not_in_cache(self, cache_get, cache_set):
        decorator = decorators.throttle_view(
            methods=['POST', 'PUT'], duration=30)
        mocked = decorator(dummy_view)
        response = mocked(self.request)
        eq_(cache_get.called, False)
        eq_(cache_set.called, False)
        eq_(response, 'ok')

    @patch('django.core.cache.cache.set', return_value=True)
    @patch('django.core.cache.cache.get', return_value=True)
    def test_other_method_in_cache(self, cache_get, cache_set):
        decorator = decorators.throttle_view(
            methods=['POST', 'PUT'], duration=30)
        mocked = decorator(dummy_view)
        response = mocked(self.request)
        eq_(cache_get.called, False)
        eq_(cache_set.called, False)
        eq_(response, 'ok')

    @patch('django.core.cache.cache.set', return_value=True)
    @patch('django.core.cache.cache.get', return_value=True)
    def test_prefix_is_used(self, cache_get, cache_set):
        decorator = decorators.throttle_view(
            methods=['GET'], duration=30, prefix='FOO')
        mocked = decorator(dummy_view)
        mocked(self.request)
        key = 'FOO%s' % self.key
        cache_get.assert_called_with(key)
        eq_(cache_set.called, False)


class TestGetRequestKey(TestCase):

    def test_user_id_is_used(self):
        user = utils.get_user_mock()
        user.pk = 4
        request = utils.get_request('get', '/foo/', user=user)
        key = decorators.get_request_key(request)
        eq_(key, '70e69f28d62ccfea7e6e9d0783bdd8d3')

    def test_http_x_forwarded_for_is_used(self):
        request = utils.get_request('get', '/foo/', user=utils.get_anon_mock())
        request.META['HTTP_X_FORWARDED_FOR'] = '8.8.8.8'
        key = decorators.get_request_key(request)
        eq_(key, 'f1327cab63da54e1dcdf5e43eca03a4a')

    def test_x_forwarded_for_is_used(self):
        request = utils.get_request('get', '/foo/', user=utils.get_anon_mock())
        request.META['X_FORWARDED_FOR'] = '8.8.8.8'
        key = decorators.get_request_key(request)
        eq_(key, 'f1327cab63da54e1dcdf5e43eca03a4a')

    def test_remote_addr_is_used(self):
        request = utils.get_request('get', '/foo/', user=utils.get_anon_mock())
        request.META['REMOTE_ADDR'] = '8.8.8.8'
        key = decorators.get_request_key(request)
        eq_(key, 'f1327cab63da54e1dcdf5e43eca03a4a')

    def test_fallback_is_used(self):
        request = utils.get_request('get', '/foo/', user=utils.get_anon_mock())
        key = decorators.get_request_key(request)
        eq_(key, '7e0c041b0a5b439e3c97b07eeffac326')
