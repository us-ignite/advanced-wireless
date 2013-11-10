from mock import patch, Mock
from nose.tools import eq_, ok_, assert_raises, raises

from django.contrib.auth.models import User, AnonymousUser
from django.http import Http404
from django.test import client, TestCase

from us_ignite.apps import views
from us_ignite.apps. models import Application
from us_ignite.apps.tests import fixtures
from us_ignite.common.tests import utils
from us_ignite.profiles.tests.fixtures import get_user


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


def _teardown_apps():
    for model in [User, Application]:
        model.objects.all().delete()


class TestAppListView(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def test_application_context_is_valid(self):
        response = views.app_list(self.factory.get('/app/'))
        eq_(sorted(response.context_data.keys()),
            ['order', 'order_form', 'page'])

    def test_non_published_applications_are_not_shown(self):
        fixtures.get_application(
            name='Gigabit app', status=Application.DRAFT)
        response = views.app_list(self.factory.get('/app/'))
        eq_(response.status_code, 200)
        eq_(len(response.context_data['page'].object_list), 0)
        _teardown_apps()

    def test_published_applications_are_listed(self):
        app = fixtures.get_application(
            name='Gigabit app', status=Application.PUBLISHED)
        response = views.app_list(self.factory.get('/app/'))
        eq_(response.status_code, 200)
        eq_(list(response.context_data['page'].object_list), [app])
        _teardown_apps()

    def test_applications_are_sorted(self):
        owner = get_user('us-ignite')
        app_a = fixtures.get_application(
            name='alpha app', status=Application.PUBLISHED, owner=owner)
        app_b = fixtures.get_application(
            name='beta app', status=Application.PUBLISHED, owner=owner)
        response = views.app_list(self.factory.get('/app/', {'order': 'name'}))
        eq_(list(response.context_data['page'].object_list), [app_a, app_b])
        _teardown_apps()

    def test_applications_are_reverse_sorted(self):
        owner = get_user('us-ignite')
        app_a = fixtures.get_application(
            name='alpha app', status=Application.PUBLISHED, owner=owner)
        app_b = fixtures.get_application(
            name='beta app', status=Application.PUBLISHED, owner=owner)
        response = views.app_list(self.factory.get('/app/', {'order': '-name'}))
        eq_(list(response.context_data['page'].object_list), [app_b, app_a])
        _teardown_apps()


def _get_message_payload(**kwargs):
    defaults = {
        'name': 'Gigabig App.',
        'description': 'An awesome gigabit app.',
        'status': Application.PUBLISHED,
    }
    defaults.update(kwargs)
    return defaults


class TestAppAddViewAnon(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def test_anon_get_request_require_login(self):
        request = self.factory.get('/app/add/')
        request.user = _get_anon_mock()
        response = views.app_add(request)
        eq_(response['Location'], utils.get_login_url('/app/add/'))

    def test_application_post_request_require_login(self):
        request = self.factory.post('/app/add/', _get_message_payload())
        request.user = _get_anon_mock()
        response = views.app_add(request)
        eq_(response['Location'], utils.get_login_url('/app/add/'))


patch_form_save = patch('us_ignite.apps.forms.ApplicationForm.save')


class TestAppAddView(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def test_get_request_is_successful(self):
        request = self.factory.get('/app/add/')
        request.user = _get_user_mock()
        response = views.app_add(request)
        eq_(response.status_code, 200)
        eq_(sorted(response.context_data.keys()),['form'])
        eq_(response.template_name, 'apps/object_add.html')

    @patch_form_save
    def test_empty_post_request_fails(self, save_mock):
        request = self.factory.post('/app/add/', {})
        request.user = _get_user_mock()
        response = views.app_add(request)
        eq_(response.status_code, 200)
        ok_(response.context_data['form'].errors)
        eq_(save_mock.call_count, 0)

    @patch_form_save
    def test_simple_post_request_succeeds(self, save_mock):
        request = self.factory.post('/app/add/', _get_message_payload())
        request.user = _get_user_mock()
        mock_instance = save_mock.return_value
        mock_instance.get_absolute_url.return_value = '/app/slug/'
        response = views.app_add(request)
        eq_(response.status_code, 302)
        eq_(response['Location'], '/app/slug/')
        save_mock.assert_called_once_with(commit=False)
        eq_(mock_instance.owner, request.user)
        mock_instance.save.assert_called_once()


class TestGetAppForUserHelper(TestCase):

    @raises(Http404)
    def test_application_does_not_exist(self):
        views.get_app_for_user('app-slug', AnonymousUser())

    @raises(Http404)
    def test_app_is_not_visible(self):
        mock_app = Mock(spec=Application)()
        mock_app.is_visible_by.return_value = False
        mock_user = Mock(spec=User)()
        with patch('us_ignite.apps.views.get_object_or_404',
                   return_value=mock_app):
            views.get_app_for_user('gigabit-app', mock_user)
            mock_app.is_visible_by.assert_called_once_with(mock_user)

    def test_app_is_visible(self):
        mock_app = Mock(spec=Application)()
        mock_app.is_visible_by.return_value = True
        mock_user = Mock(spec=User)()
        with patch('us_ignite.apps.views.get_object_or_404',
                   return_value=mock_app):
            response = views.get_app_for_user('gigabit-app', mock_user)
            mock_app.is_visible_by.assert_called_once_with(mock_user)
            eq_(response, mock_app)


class TestAppDetailView(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    @raises(Http404)
    def test_missing_app_raises_404(self):
        request = self.factory.get('/apps/foo/')
        request.user = AnonymousUser()
        with patch('us_ignite.apps.views.get_app_for_user',
                   side_effect=Http404) as get_mock:
            views.app_detail(request, 'foo')
            get_mock.assert_once_called_with('foo', request.user)

    def test_app_detail_is_valid(self):
        request = self.factory.get('/apps/foo/')
        request.user = AnonymousUser()
        mock_app = Mock(spec=Application)()
        with patch('us_ignite.apps.views.get_app_for_user',
                   return_value=mock_app) as get_mock:
            response = views.app_detail(request, 'foo')
            eq_(sorted(response.context_data.keys()), ['object'])
            eq_(response.template_name, 'apps/object_detail.html')
            get_mock.assert_once_called_with('foo', request.user)
