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
            sorted(['object', 'member_list', 'is_member', 'is_guardian']))

    @raises(Http404)
    def test_unpublished_hub_request_fails(self):
        fixtures.get_hub(name='community', status=models.Hub.DRAFT)
        request = utils.get_request(
            'get', '/hub/community/', user=utils.get_anon_mock())
        views.hub_detail(request, 'community')

    def test_guardian_unpublished_request_succeeds(self):
        guardian = get_user('guardian')
        hub = fixtures.get_hub(name='community', status=models.Hub.DRAFT,
                               guardian=guardian)
        request = utils.get_request('get', '/hub/community/', user=guardian)
        response = views.hub_detail(request, 'community')
        eq_(response.status_code, 200)
        eq_(sorted(response.context_data.keys()),
            sorted(['object', 'member_list', 'is_member', 'is_guardian']))


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
    def test_not_guardian_request_fails(self):
        user = get_user('us-ignite')
        fixtures.get_hub(name='community', status=models.Hub.PUBLISHED)
        request = utils.get_request('get', '/hub/community/edit/', user=user)
        views.hub_edit(request, 'community')

    def test_guardian_request_is_successful(self):
        guardian = get_user('guardian')
        hub = fixtures.get_hub(
            name='community', status=models.Hub.PUBLISHED, guardian=guardian)
        request = utils.get_request(
            'get', '/hub/community/edit/', user=guardian)
        response = views.hub_edit(request, 'community')
        eq_(response.status_code, 200)
        eq_(response.template_name, 'hubs/object_edit.html')
        eq_(sorted(response.context_data.keys()), sorted(['form', 'object']))
        eq_(response.context_data['object'], hub)

    def test_guardian_update_is_successful(self):
        guardian = get_user('guardian')
        hub = fixtures.get_hub(
            name='community', status=models.Hub.PUBLISHED, guardian=guardian)
        data = {
            'name': 'New name!',
            'description': 'New description.'
        }
        request = utils.get_request(
            'post', '/hub/community/edit/', data=data, user=guardian)
        request._messages = utils.TestMessagesBackend(request)
        response = views.hub_edit(request, 'community')
        eq_(response.status_code, 302)
        eq_(response['Location'], hub.get_absolute_url())
        eq_(models.Hub.objects.values('name').get(slug='community'),
            {'name': 'New name!'})


class TestHubListView(TestCase):

    def test_get_request_is_successful(self):
        user = utils.get_anon_mock()
        request = utils.get_request('get', '/hub/', user=user)
        response = views.hub_list(request)
        eq_(response.status_code, 200)
        eq_(response.template_name, 'hubs/object_list.html')
        eq_(sorted(response.context_data.keys()), ['object_list'])
