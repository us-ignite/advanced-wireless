from django.test import client, TestCase
from django.contrib.auth.models import Group, User

from mock import Mock
from nose.tools import eq_, ok_, raises

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
        request = self.factory.get('/')
        view = decorators.group_required()(dummy_view)

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
        ok_('unavailable' in response.content.lower())

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
