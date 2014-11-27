from mock import patch, Mock
from nose.tools import eq_, ok_, raises

from django.contrib.auth.models import User
from django.http import Http404
from django.test import TestCase

from us_ignite.common.tests import utils
from us_ignite.profiles.tests.fixtures import get_user
from us_ignite.hubs import models, views
from us_ignite.hubs.tests import fixtures


patch_hub_request_filter = patch(
    'us_ignite.hubs.models.HubRequest.objects.filter')
patch_hub_request_form_save = patch('us_ignite.hubs.forms.HubRequestForm.save')
patch_notify_request = patch('us_ignite.hubs.mailer.notify_request')
patch_get_object = patch('us_ignite.hubs.views.get_object_or_404')


class TestHubApplicationView(TestCase):

    def test_hub_application_requires_login(self):
        request = utils.get_request(
            'get', '/hub/apply/', user=utils.get_anon_mock())
        response = views.hub_application(request)
        eq_(response.status_code, 302)
        eq_(response['Location'], utils.get_login_url('/hub/apply/'))

    @patch_hub_request_filter
    def test_get_request_is_successful(self, mock_filter):
        request = utils.get_request(
            'get', '/hub/apply/', user=utils.get_user_mock())
        response = views.hub_application(request)
        eq_(response.status_code, 200)
        eq_(sorted(response.context_data.keys()), ['form', 'object_list'])
        eq_(response.template_name, 'hubs/object_application.html')
        mock_filter.assert_called_once()

    @patch_hub_request_filter
    def test_empty_submission_fails(self, *args):
        request = utils.get_request(
            'post', '/hub/apply/', data={}, user=utils.get_user_mock())
        response = views.hub_application(request)
        eq_(response.status_code, 200)
        eq_(sorted(response.context_data.keys()), ['form', 'object_list'])
        eq_(response.template_name, 'hubs/object_application.html')
        ok_(response.context_data['form'].errors)

    @patch_hub_request_filter
    @patch_notify_request
    @patch_hub_request_form_save
    def test_submission_is_successful(self, mock_save, mock_notify, *args):
        mock_instance = Mock(spec=models.HubRequest)()
        mock_save.return_value = mock_instance
        data = {
            'name': 'Gigabit community',
            'description': 'Community description.',
        }
        user = utils.get_user_mock()
        request = utils.get_request(
            'post', '/hub/apply/', data=data, user=user)
        request._messages = utils.TestMessagesBackend(request)
        response = views.hub_application(request)
        mock_save.assert_called_once_with(commit=False)
        mock_instance.assert_called_once()
        mock_notify.assert_called_once_with(mock_instance)
        eq_(response.status_code, 302)
        eq_(response['Location'], '/')


class TestHubDetailView(TestCase):

    def tearDown(self):
        for model in [models.Hub, User]:
            model.objects.all().delete()

    def test_published_hub_request_is_successful(self):
        fixtures.get_hub(name='community', status=models.Hub.PUBLISHED)
        request = utils.get_request(
            'get', '/hub/community/', user=utils.get_anon_mock())
        response = views.hub_detail(request, 'community')
        eq_(response.status_code, 200)
        eq_(sorted(response.context_data.keys()),
            sorted(['activity_list', 'award_list', 'event_list',
                    'feature_list', 'is_contact', 'is_member',
                    'member_list', 'object', 'testbed_list', 'url_list',
                    'application_list'])
        )

    @raises(Http404)
    def test_unpublished_hub_request_fails(self):
        fixtures.get_hub(name='community', status=models.Hub.DRAFT)
        request = utils.get_request(
            'get', '/hub/community/', user=utils.get_anon_mock())
        views.hub_detail(request, 'community')

    def test_contact_unpublished_request_succeeds(self):
        contact = get_user('contact')
        hub = fixtures.get_hub(name='community', status=models.Hub.DRAFT,
                               contact=contact)
        request = utils.get_request('get', '/hub/community/', user=contact)
        response = views.hub_detail(request, 'community')
        eq_(response.status_code, 200)
        eq_(sorted(response.context_data.keys()),
            sorted(['activity_list', 'award_list', 'event_list',
                    'feature_list', 'is_contact', 'is_member',
                    'member_list', 'object', 'testbed_list', 'url_list',
                    'application_list'])
        )


class TestHubMembershipView(TestCase):

    def tearDown(self):
        for model in [models.Hub, User]:
            model.objects.all().delete()

    def test_membership_requires_a_post_request(self):
        request = utils.get_request(
            'get', '/hub/community/membership/', user=utils.get_anon_mock())
        response = views.hub_membership(request, 'community')
        eq_(response.status_code, 405)

    def test_membership_requires_authentication(self):
        request = utils.get_request(
            'post', '/hub/community/membership/', user=utils.get_anon_mock())
        response = views.hub_membership(request, 'community')
        eq_(response.status_code, 302)
        eq_(response['Location'],
            utils.get_login_url('/hub/community/membership/'))

    def test_membership_request_is_successful(self):
        member = get_user('member')
        hub = fixtures.get_hub(name='community', status=models.Hub.PUBLISHED)
        request = utils.get_request(
            'post', '/hub/community/', data={}, user=member)
        request._messages = utils.TestMessagesBackend(request)
        response = views.hub_membership(request, 'community')
        eq_(response.status_code, 302)
        eq_(response['Location'], hub.get_absolute_url())
        ok_(models.HubMembership.objects.get(user=member, hub=hub))


def _get_hub_inline_payload(pk, data_list=None, **kwargs):
    data_list = data_list if data_list else [{}]
    prefix = 'huburl_set-'
    default = {
        '%sTOTAL_FORMS' % prefix: len(data_list),
        '%sINITIAL_FORMS' % prefix: 0,
        '%sMAX_NUM_FORMS' % prefix: 3,
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


class TestHubEditView(TestCase):

    def tearDown(self):
        for model in [models.Hub, User]:
            model.objects.all().delete()

    def test_anon_request_fails(self):
        user = utils.get_anon_mock()
        request = utils.get_request('get', '/hub/community/edit/', user=user)
        response = views.hub_edit(request, 'community')
        eq_(response.status_code, 302)
        eq_(response['Location'], utils.get_login_url('/hub/community/edit/'))

    @raises(Http404)
    def test_not_contact_request_fails(self):
        user = get_user('us-ignite')
        fixtures.get_hub(name='community', status=models.Hub.PUBLISHED)
        request = utils.get_request('get', '/hub/community/edit/', user=user)
        views.hub_edit(request, 'community')

    def test_contact_request_is_successful(self):
        contact = get_user('contact')
        hub = fixtures.get_hub(
            name='community', status=models.Hub.PUBLISHED, contact=contact)
        request = utils.get_request(
            'get', '/hub/community/edit/', user=contact)
        response = views.hub_edit(request, 'community')
        eq_(response.status_code, 200)
        eq_(response.template_name, 'hubs/object_edit.html')
        eq_(sorted(response.context_data.keys()),
            sorted(['form', 'object', 'link_formset']))
        eq_(response.context_data['object'], hub)

    def test_contact_update_is_successful(self):
        contact = get_user('contact')
        hub = fixtures.get_hub(
        name='community', status=models.Hub.PUBLISHED, contact=contact)
        data = {
            'name': 'New name!',
            'description': 'New description.'
        }
        data.update(_get_hub_inline_payload(hub.pk))
        request = utils.get_request(
            'post', '/hub/community/edit/', data=data, user=contact)
        request._messages = utils.TestMessagesBackend(request)
        response = views.hub_edit(request, 'community')
        eq_(response.status_code, 302)
        eq_(response['Location'], hub.get_absolute_url())
        eq_(models.Hub.objects.values('name').get(slug='community'),
            {'name': 'New name!'})


class TestHubListView(TestCase):

    @patch('us_ignite.hubs.models.Hub.active.all')
    def test_get_request_is_successful(self, all_mock):
        user = utils.get_anon_mock()
        request = utils.get_request('get', '/hub/', user=user)
        response = views.hub_list(request)
        eq_(response.status_code, 200)
        eq_(response.template_name, 'hubs/object_list.html')
        eq_(sorted(response.context_data.keys()),
            sorted(['page', 'featured_list']))
        all_mock.assert_called_once_with()


class TestHubLocationsJSON(TestCase):

    @patch('us_ignite.hubs.views.get_app_member_list')
    @patch('us_ignite.hubs.views.get_users')
    @patch('us_ignite.hubs.views.get_location_dict')
    @patch_get_object
    @patch('us_ignite.hubs.views.get_event_list')
    def test_hub_locations_json(
            self, mock_list, mock_hub, mock_location, mock_user, mock_member):
        mock_list.return_value = []
        mock_hub.return_value = 'foo'
        mock_location.return_value = None
        mock_user.return_value = []
        mock_member.return_value = []
        request = utils.get_request('get', '/hub/foo/')
        response = views.hub_locations_json(request, 'foo')
        eq_(response.status_code, 200)
        eq_(response['Content-Type'], 'application/javascript')
        mock_hub.assert_called_once_with(models.Hub.active, slug__exact='foo')
        mock_list.asset_called_once_with('foo')
