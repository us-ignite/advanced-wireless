from mock import patch, Mock
from nose.tools import eq_, ok_, assert_raises, raises

from django.contrib.auth.models import User, AnonymousUser
from django.http import Http404
from django.test import client, TestCase

from us_ignite.apps import views, forms
from us_ignite.apps.models import (Application, ApplicationURL, Page,
                                   ApplicationMembership, ApplicationVersion)
from us_ignite.apps.tests import fixtures
from us_ignite.common.tests import utils
from us_ignite.hubs.models import Hub, HubAppMembership
from us_ignite.hubs.tests.fixtures import get_hub
from us_ignite.profiles.tests.fixtures import get_user


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
        'summary': 'This app is great!',
        'status': Application.PUBLISHED,
        'stage': Application.IDEA,
    }
    defaults.update(kwargs)
    return defaults


def _get_applinks_inline_payload(pk, data_list=None, **kwargs):
    """Generates the inline payload for the ``ApplicationLinks``."""
    data_list = data_list if data_list else [{}]
    prefix = 'applicationurl_set-'
    default = {
        '%sTOTAL_FORMS' % prefix: len(data_list),
        '%sINITIAL_FORMS' % prefix: 0,
        '%sMAX_NUM_FORMS'% prefix: 3,
    }
    _inline_tuple = lambda i, k, v: ('%s%s-%s' % (prefix, i, k), v)
    for i, inline in enumerate(data_list):
        inline_default = {
            '%s%s-DELETE' % (prefix, i): '',
            '%s%s-application' % (prefix, i): pk,
        }
        inline_item = dict(_inline_tuple(i, k, v) for k, v in inline.items())
        inline_default.update(inline_item)
        default.update(inline_default)
    default.update(kwargs)
    return default


def _get_appimages_inline_payload(pk, data_list=None, **kwargs):
    """Generates the inline payload for the ``ApplicationImages``."""
    data_list = data_list if data_list else [{}]
    prefix = 'applicationimage_set-'
    default = {
        '%sTOTAL_FORMS' % prefix: len(data_list),
        '%sINITIAL_FORMS' % prefix: 0,
        '%sMAX_NUM_FORMS'% prefix: 3,
    }
    _inline_tuple = lambda i, k, v: ('%s%s-%s' % (prefix, i, k), v)
    for i, inline in enumerate(data_list):
        inline_default = {
            '%s%s-DELETE' % (prefix, i): '',
            '%s%s-application' % (prefix, i): pk,
        }
        inline_item = dict(_inline_tuple(i, k, v) for k, v in inline.items())
        inline_default.update(inline_item)
        default.update(inline_default)
    default.update(kwargs)
    return default


class TestAppAddViewAnon(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def test_anon_get_request_require_login(self):
        request = self.factory.get('/app/add/')
        request.user = utils.get_anon_mock()
        response = views.app_add(request)
        eq_(response['Location'], utils.get_login_url('/app/add/'))

    def test_application_post_request_require_login(self):
        request = self.factory.post('/app/add/', _get_message_payload())
        request.user = utils.get_anon_mock()
        response = views.app_add(request)
        eq_(response['Location'], utils.get_login_url('/app/add/'))


patch_form_save = patch('us_ignite.apps.forms.ApplicationForm.save')


class TestAppAddView(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def test_get_request_is_successful(self):
        request = self.factory.get('/app/add/')
        request.user = utils.get_user_mock()
        response = views.app_add(request)
        eq_(response.status_code, 200)
        eq_(sorted(response.context_data.keys()), ['form'])
        eq_(response.template_name, 'apps/object_add.html')

    @patch_form_save
    def test_empty_post_request_fails(self, save_mock):
        request = self.factory.post('/app/add/', {})
        request.user = utils.get_user_mock()
        response = views.app_add(request)
        eq_(response.status_code, 200)
        ok_(response.context_data['form'].errors)
        eq_(save_mock.call_count, 0)

    @patch_form_save
    @patch.object(forms.ApplicationForm, 'save_m2m', create=True)
    def test_simple_post_request_succeeds(self, save_m2m_mock, save_mock):
        request = self.factory.post('/app/add/', _get_message_payload())
        request._messages = utils.TestMessagesBackend(request)
        request.user = utils.get_user_mock()
        mock_instance = save_mock.return_value
        mock_instance.get_absolute_url.return_value = '/app/slug/'
        response = views.app_add(request)
        eq_(response.status_code, 302)
        eq_(response['Location'], '/app/slug/')
        save_mock.assert_called_once_with(commit=False)
        eq_(mock_instance.owner, request.user)
        mock_instance.save.assert_called_once()
        save_m2m_mock.assert_called_once()

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

    @patch('us_ignite.apps.views.get_app_for_user')
    def test_app_detail_is_valid(self, get_mock):
        request = self.factory.get('/apps/foo/')
        request.user = AnonymousUser()
        mock_app = Mock(spec=Application)()
        get_mock.return_value = mock_app
        response = views.app_detail(request, 'foo')
        eq_(sorted(response.context_data.keys()),
            ['award_list', 'can_edit', 'feature_list', 'image_list', 'is_owner',
             'member_list', 'object', 'url_list', 'version_list'])
        eq_(response.template_name, 'apps/object_detail.html')
        get_mock.assert_once_called_with('foo', request.user)


class TestAppEditViewAnon(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def test_anon_get_request_require_login(self):
        request = self.factory.get('/app/my-app/edit/')
        request.user = utils.get_anon_mock()
        response = views.app_edit(request)
        eq_(response['Location'], utils.get_login_url('/app/my-app/edit/'))

    def test_application_post_request_require_login(self):
        request = self.factory.post('/app/my-app/edit/', _get_message_payload())
        request.user = utils.get_anon_mock()
        response = views.app_edit(request)
        eq_(response['Location'], utils.get_login_url('/app/my-app/edit/'))


class TestAppEditView(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def _get_request(self, url='/app/my-app/edit/'):
        request = self.factory.get(url)
        request.user = utils.get_user_mock()
        return request

    @raises(Http404)
    def test_non_existing_app_raises_404(self):
        request = self._get_request()
        with patch('us_ignite.apps.views.get_object_or_404',
                   side_effect=Http404) as get_mock:
            views.app_edit(request, 'my-app')
            get_mock.assert_called_once_with(
                Application.active, slug__exact='my-app')

    @raises(Http404)
    def test_non_editable_app_raises_404(self):
        request = self._get_request()
        mock_app = Mock(spec=Application)()
        mock_app.is_editable_by.return_value = False
        with patch('us_ignite.apps.views.get_object_or_404',
                   return_value=mock_app) as get_mock:
            views.app_edit(request, 'my-app')
            mock_app.is_editable_by.assert_called_once_with(request.user)


class TestAppEditViewWithData(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def tearDown(self):
        for model in [Application]:
            model.objects.all().delete()

    def test_get_request_is_successful(self):
        owner = get_user('us-ignite')
        app = fixtures.get_application(
            slug='alpha', status=Application.PUBLISHED, owner=owner)
        request = self.factory.get('/app/alpha/')
        request.user = owner
        response = views.app_edit(request, 'alpha')
        eq_(sorted(response.context_data.keys()),
            ['form', 'image_formset', 'link_formset', 'object'])
        eq_(response.template_name, 'apps/object_edit.html')

    def test_post_request_is_successful(self):
        owner = get_user('us-ignite')
        app = fixtures.get_application(
            slug='beta', status=Application.PUBLISHED, owner=owner)
        payload = _get_message_payload(name='Updated')
        payload.update(_get_applinks_inline_payload(app.id))
        payload.update(_get_appimages_inline_payload(app.id))
        request = self.factory.post('/app/beta/', payload)
        request._messages = utils.TestMessagesBackend(request)
        request.user = owner
        response = views.app_edit(request, 'beta')
        eq_(response.status_code, 302)
        eq_(response['Location'], app.get_absolute_url())
        eq_(Application.objects.values('name').get(owner=owner),
            {'name': 'Updated'})
        eq_(ApplicationURL.objects.filter(application=app).count(), 0)

    def test_post_request_saves_urls(self):
        owner = get_user('us-ignite')
        app = fixtures.get_application(
            slug='beta', status=Application.PUBLISHED, owner=owner)
        payload = _get_message_payload()
        links = [
            {'name': 'github', 'url': 'http://github.com'},
            {'name': 'twitter', 'url': 'http://twitter.com'},
        ]
        payload.update(_get_applinks_inline_payload(app.id, data_list=links))
        payload.update(_get_appimages_inline_payload(app.id))
        request = self.factory.post('/app/beta/', payload)
        request._messages = utils.TestMessagesBackend(request)
        request.user = owner
        response = views.app_edit(request, 'beta')
        eq_(response.status_code, 302)
        eq_(response['Location'], app.get_absolute_url())
        eq_(ApplicationURL.objects.filter(application=app).count(), 2)


class TestAppVersion(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def _teardown(self):
        for model in [User, Application]:
            model.objects.all().delete()

    def test_anon_get_request_is_forbidden(self):
        request = self.factory.get('/app/app/version/')
        request.user = utils.get_anon_mock()
        response = views.app_version_add(request)
        eq_(response.status_code, 405)

    def test_anon_post_requires_login(self):
        request = self.factory.post('/app/app/version/', {})
        request.user = utils.get_anon_mock()
        response = views.app_version_add(request)
        expected_url = utils.get_login_url('/app/app/version/')
        eq_(response['Location'], expected_url)

    @raises(Http404)
    @patch('us_ignite.apps.views.get_object_or_404')
    def test_non_existing_app_or_owner_raises_404(self, mock_get):
        mock_get.side_effect = Http404
        request = self.factory.post('/app/app/version/', {})
        request.user = utils.get_user_mock()
        views.app_version_add(request, 'app')

    @patch('us_ignite.apps.models.ApplicationVersion.objects.create_version')
    @patch('us_ignite.apps.views.get_object_or_404')
    def test_versioning_is_successful(self, mock_get, mock_create):
        app_mock = Mock(spec=Application)
        app_mock.name = 'Gigabit'
        app_mock.get_absolute_url.return_value = '/app/app/'
        mock_get.return_value = app_mock
        request = self.factory.post('/app/app/version/', {})
        request.user = utils.get_user_mock()
        request._messages = utils.TestMessagesBackend(request)
        response = views.app_version_add(request, 'app')
        mock_create.assert_called_once_with(app_mock)
        eq_(response.status_code, 302)
        eq_(response['Location'], '/app/app/')


class TestAppVersionDetailView(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    @raises(Http404)
    @patch('us_ignite.apps.views.get_app_for_user')
    def test_missing_app_raises_404(self, get_mock):
        get_mock.side_effect = Http404
        request = self.factory.get('/apps/gigabit/version/1/')
        request.user = AnonymousUser()
        views.app_version_detail(request, 'gigabit', '1')
        get_mock.assert_once_called_with('foo', request.user)

    @patch('us_ignite.apps.views.get_app_for_user')
    def test_missing_version_raises_404(self, get_mock):
        app_mock = Mock(spec=Application)
        app_mock.applicationversion_set.all.return_value = []
        get_mock.return_value = app_mock
        request = self.factory.get('/apps/gigabit/version/1/')
        request.user = AnonymousUser()
        assert_raises(Http404, views.app_version_detail, request, 'gigabit', '1')
        get_mock.assert_called_once_with('gigabit', request.user)
        app_mock.applicationversion_set.all.assert_called_once()

    @patch('us_ignite.apps.views.get_app_for_user')
    def test_version_renders_successfully(self, get_mock):
        app_mock = Mock(spec=Application)
        version_mock = Mock(spec=ApplicationVersion)
        version_mock.slug = '1'
        app_mock.applicationversion_set.all.return_value = [version_mock]
        get_mock.return_value = app_mock
        request = self.factory.get('/apps/gigabit/version/1/')
        request.user = AnonymousUser()
        response = views.app_version_detail(request, 'gigabit', '1')
        get_mock.assert_called_once_with('gigabit', request.user)
        app_mock.applicationversion_set.all.assert_called_once()
        eq_(sorted(response.context_data.keys()),
            ['app', 'object', 'version_list'])
        eq_(response.template_name, 'apps/object_version_detail.html')


class TestAppMembershipView(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def _teardown(self):
        for model in [User, Application]:
            model.objects.all().delete()

    def test_anon_get_request_require_login(self):
        request = self.factory.get('/app/b/membership/')
        request.user = utils.get_anon_mock()
        response = views.app_membership(request)
        eq_(response['Location'], utils.get_login_url('/app/b/membership/'))

    def test_application_post_request_require_login(self):
        request = self.factory.post('/app/b/membership/', {})
        request.user = utils.get_anon_mock()
        response = views.app_membership(request)
        eq_(response['Location'], utils.get_login_url('/app/b/membership/'))

    @raises(Http404)
    def test_non_existing_app_or_owner_raises_404_on_get(self):
        request = self.factory.get('/app/b/membership/')
        request.user = utils.get_user_mock()
        with patch('us_ignite.apps.views.get_object_or_404',
                   side_effect=Http404) as get_mock:
            views.app_membership(request, 'b')
            get_mock.assert_called_once_with(
                Application.active, slug__exact='b', owner=request.user)

    @raises(Http404)
    def test_non_existing_app_or_owner_raises_404_on_post(self):
        request = self.factory.post('/app/b/membership/', {})
        request.user = utils.get_user_mock()
        with patch('us_ignite.apps.views.get_object_or_404',
                   side_effect=Http404) as get_mock:
            views.app_membership(request, 'b')
            get_mock.assert_called_once_with(
                Application.active, slug__exact='b', owner=request.user)

    def test_valid_membership_get_request_is_successful(self):
        owner = get_user('owner')
        app = fixtures.get_application(
            slug='gamma', status=Application.PUBLISHED, owner=owner)
        request = self.factory.get('/app/gamma/membership/')
        request.user = owner
        response = views.app_membership(request, 'gamma')
        eq_(response.status_code, 200)
        eq_(sorted(response.context_data.keys()),
            ['form', 'membership_list', 'object'])
        eq_(response.context_data['object'], app)
        self._teardown()

    def test_valid_membership_empty_payload_fails(self):
        owner = get_user('owner')
        fixtures.get_application(
            slug='gamma', status=Application.PUBLISHED, owner=owner)
        request = self.factory.post('/app/gamma/membership/', {})
        request.user = owner
        response = views.app_membership(request, 'gamma')
        eq_(response.status_code, 200)
        ok_(response.context_data['form'].errors)
        self._teardown()

    def test_valid_membership_adds_user(self):
        owner = get_user('owner')
        member = get_user('member', email='member@us-ignite.org')
        app = fixtures.get_application(
            slug='delta', status=Application.PUBLISHED, owner=owner)
        request = self.factory.post(
            '/app/delta/membership/', {'collaborators': 'member@us-ignite.org'})
        request.user = owner
        request._messages = utils.TestMessagesBackend(request)
        response = views.app_membership(request, 'delta')
        ok_(app.members.get(id=member.id))
        eq_(response.status_code, 302)
        eq_(response['Location'], app.get_membership_url())


class TestAppMembershipRemovalView(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def _teardown(self):
        for model in [User, Application]:
            model.objects.all().delete()

    def test_anon_get_request_is_forbidden(self):
        request = self.factory.get('/app/b/membership/remove/1/')
        request.user = utils.get_anon_mock()
        response = views.app_membership_remove(request)
        eq_(response.status_code, 405)

    def test_anon_post_requires_login(self):
        request = self.factory.post('/app/b/membership/remove/1/', {})
        request.user = utils.get_anon_mock()
        response = views.app_membership_remove(request)
        expected_url = utils.get_login_url('/app/b/membership/remove/1/')
        eq_(response['Location'], expected_url)

    @raises(Http404)
    def test_non_existing_app_or_owner_raises_404(self):
        request = self.factory.post('/app/b/membership/remove/1/', {})
        request.user = utils.get_user_mock()
        with patch('us_ignite.apps.views.get_object_or_404',
                   side_effect=Http404) as get_mock:
            views.app_membership_remove(request, 'b', 1)
            get_mock.assert_called_once_with(
                ApplicationMembership.objects.select_related('application'),
                application__slug__exact='b', application__owner=request.user, pk=1)

    def test_removal_request_is_successful(self):
        owner = get_user('owner')
        app = fixtures.get_application(
            slug='zeta', status=Application.PUBLISHED, owner=owner)
        membership = fixtures.get_membership(application=app, user=owner)
        url = '/app/zeta/membership/remove/%s/' % membership.id
        request = self.factory.post(url, {})
        request.user = owner
        request._messages = utils.TestMessagesBackend(request)
        response = views.app_membership_remove(request, 'zeta', membership.id)
        eq_(response.status_code, 302)
        eq_(response['Location'], app.get_membership_url())
        eq_(ApplicationMembership.objects.all().count(), 0)


class TestFeaturedApplicationView(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    @raises(Http404)
    @patch('us_ignite.apps.views.get_object_or_404')
    def test_page_does_not_exist(self, get_mock):
        get_mock.side_effect = Http404
        request = self.factory.get('/featured/')
        views.apps_featured(request)

    @patch('us_ignite.apps.views.get_object_or_404')
    def test_page_request_is_successful(self, mock_get):
        mock_page = mock_get.return_value
        mock_page.pageapplication_set.all.return_value = []
        request = self.factory.get('/featured/')
        response = views.apps_featured(request)
        eq_(response.status_code, 200)
        eq_(sorted(response.context_data.keys()),
            ['application_list', 'object'])
        mock_get.assert_called_once_with(Page, status=Page.FEATURED)
        mock_page.pageapplication_set.all.assert_called_once()


class TestFeaturedApplicationArchiveView(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    @raises(Http404)
    @patch('us_ignite.apps.views.get_object_or_404')
    def test_page_does_not_exist(self, get_mock):
        get_mock.side_effect = Http404
        request = self.factory.get('/featured/archive/slug/')
        views.apps_featured_archive(request, 'slug')

    @patch('us_ignite.apps.views.get_object_or_404')
    def test_page_request_is_successful(self, mock_get):
        mock_page = mock_get.return_value
        mock_page.pageapplication_set.all.return_value = []
        request = self.factory.get('/featured/archive/slug/')
        response = views.apps_featured_archive(request, 'slug')
        eq_(response.status_code, 200)
        eq_(sorted(response.context_data.keys()),
            ['application_list', 'object'])
        mock_get.assert_called_once_with(
            Page, status=Page.PUBLISHED, slug__exact='slug')
        mock_page.pageapplication_set.all.assert_called_once()


class TestAppExportView(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def test_export_requires_login(self):
        request = self.factory.get('/app/blue/export/')
        request.user = utils.get_anon_mock()
        response = views.app_export(request, 'blue')
        expected_url = utils.get_login_url('/app/blue/export/')
        eq_(response['Location'], expected_url)

    @raises(Http404)
    @patch('us_ignite.apps.views.get_object_or_404')
    def test_non_active_app_raises_404(self, mock_get):
        mock_get.side_effect = Http404
        request = self.factory.get('/app/blue/export')
        request.user = utils.get_user_mock()
        views.app_export(request, 'blue')

    @patch('us_ignite.apps.views.get_object_or_404')
    def test_non_member_raises_404(self, mock_get):
        app_mock = Mock(spec=Application)
        app_mock.name = 'Gigabit'
        app_mock.has_member.return_value = False
        mock_get.return_value = app_mock
        request = self.factory.get('/app/blue/export')
        request.user = utils.get_user_mock()
        assert_raises(Http404, views.app_export, request, 'blue')
        mock_get.assert_called_once_with(Application.active, slug__exact='blue')
        app_mock.has_member.assert_called_once_with(request.user)

    @patch('us_ignite.apps.views.render_to_string')
    @patch('us_ignite.apps.views.get_object_or_404')
    def test_app_is_exported_successfully(self, mock_get, mock_render):
        mock_render.return_value = 'OK'
        app_mock = Mock(spec=Application)()
        app_mock.name = 'Gigabit'
        app_mock.has_member.return_value = True
        mock_get.return_value = app_mock
        request = self.factory.get('/app/blue/export')
        request.user = utils.get_user_mock()
        response = views.app_export(request, 'blue')
        mock_get.assert_called_once_with(Application.active, slug__exact='blue')
        mock_render.assert_called_once()
        eq_(response['Content-Type'], 'text/plain')
        ok_('attachment; filename=' in response['Content-Disposition'])
        ok_(response.content, 'OK')


class TestAppHubMembershipAnon(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def test_anon_get_request_require_login(self):
        request = self.factory.get('/app/my-app/hubs/')
        request.user = utils.get_anon_mock()
        response = views.app_hub_membership(request)
        eq_(response['Location'], utils.get_login_url('/app/my-app/hubs/'))

    def test_application_post_request_require_login(self):
        request = self.factory.post('/app/my-app/hubs/', {})
        request.user = utils.get_anon_mock()
        response = views.app_hub_membership(request)
        eq_(response['Location'], utils.get_login_url('/app/my-app/hubs/'))


class TestAppHubMembership(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def _get_request(self, url='/app/my-app/hubs/'):
        request = self.factory.get(url)
        request.user = utils.get_user_mock()
        return request

    @raises(Http404)
    @patch('us_ignite.apps.views.get_object_or_404')
    def test_non_existing_app_raises_404(self, mock_get):
        mock_get.side_effect = Http404
        request = self._get_request()
        views.app_hub_membership(request, 'my-app')
        mock_get.assert_called_once_with(
            Application.active, slug__exact='my-app')

    @patch('us_ignite.apps.views.get_object_or_404')
    def test_non_editable_app_raises_404(self, mock_get):
        mock_app = Mock(spec=Application)()
        mock_app.is_editable_by.return_value = False
        mock_get.return_value = mock_app
        request = self._get_request()
        assert_raises(Http404, views.app_hub_membership, request, 'my-app')
        mock_app.is_editable_by.assert_called_once_with(request.user)


class TestAppHubMembershipWithData(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()
        self.hub = get_hub(name='My hub.', status=Hub.PUBLISHED)
        self.user = get_user('us-ignite')

    def tearDown(self):
        for model in [Application, Hub, User]:
            model.objects.all().delete()

    def test_get_request_is_successful(self):
        app = fixtures.get_application(
            slug='alpha', status=Application.PUBLISHED, owner=self.user)
        request = self.factory.get('/app/alpha/hubs/')
        request.user = self.user
        response = views.app_hub_membership(request, 'alpha')
        eq_(response.status_code, 200)
        eq_(response.template_name, 'apps/object_hub_membership.html')
        eq_(sorted(response.context_data.keys()), ['form', 'object'])
        eq_(response.context_data['object'], app)

    def test_post_payload_is_successful(self):
        app = fixtures.get_application(
            slug='alpha', status=Application.PUBLISHED, owner=self.user)
        data = {
            'hubs': [self.hub.id],
        }
        request = self.factory.post('/app/alpha/hubs/', data)
        request.user = self.user
        request._messages = utils.TestMessagesBackend(request)
        response = views.app_hub_membership(request, 'alpha')
        eq_(response.status_code, 302)
        eq_(response['Location'], app.get_absolute_url())
        ok_(HubAppMembership.objects.get(application=app, hub=self.hub))


class TestGetMembershipForm(TestCase):

    @patch('us_ignite.apps.views.HubAppMembershipForm')
    def test_empty_membership_list_has_no_defaults(self, mock_form):
        form = views._get_membership_form([])
        hubs = form.fields['hubs']
        mock_form.assert_called_once_with()

    @patch('us_ignite.apps.views.HubAppMembershipForm')
    def test_membership_list_uses_initial_data(self, mock_form):
        mock_membership = Mock()
        mock_membership.hub.id = 1
        form = views._get_membership_form([mock_membership])
        hubs = form.fields['hubs']
        mock_form.assert_called_once_with({'hubs': [1]})


patch_membership_get = patch(
    'us_ignite.hubs.models.HubAppMembership.objects.get_or_create')


class TestUpdateMembership(TestCase):

    @patch_membership_get
    def test_membership_is_removed(self, mock_membership_get):
        app = Mock(spec=Application)()
        hub_list = []
        mock_membership = Mock(spec=HubAppMembership)()
        mock_membership.hub = 1
        mock_membership.delete.return_value = True
        membership_list = [mock_membership]
        result = views._update_membership(app, hub_list, membership_list)
        eq_(result, True)
        mock_membership.delete.assert_called_once()
        eq_(mock_membership_get.call_count, 0)

    @patch_membership_get
    def test_membership_is_kept(self, mock_membership_get):
        app = Mock(spec=Application)()
        hub_list = [1]
        mock_membership = Mock(spec=HubAppMembership)()
        mock_membership.hub = 1
        mock_membership.delete.return_value = True
        membership_list = [mock_membership]
        result = views._update_membership(app, hub_list, membership_list)
        eq_(result, True)
        eq_(mock_membership.delete.call_count, 0)
        mock_membership_get.assert_called_once_with(hub=1, application=app)
