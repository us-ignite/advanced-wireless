from nose.tools import assert_raises, eq_
from mock import patch, Mock

from django.contrib.auth.models import User
from django.http import Http404
from django.test import TestCase

from us_ignite.common.tests import utils
from us_ignite.organizations import views
from us_ignite.organizations.models import Organization, OrganizationMember
from us_ignite.organizations.tests import fixtures
from us_ignite.profiles.tests.fixtures import get_user

patch_get_object = patch('us_ignite.organizations.views.get_object_or_404')
patch_get_awards = patch('us_ignite.organizations.views.get_award_list')


class TestOrganizationDetailView(TestCase):

    @patch_get_object
    def test_organization_does_not_exist(self, mock_get):
        mock_get.side_effect = Http404
        request = utils.get_request(
            'get', '/organization/foo/', user=utils.get_anon_mock())
        assert_raises(Http404, views.organization_detail, request, 'foo')

    @patch_get_object
    def test_organization_is_not_visible(self, mock_get):
        mock_instance = Mock(spec=Organization)()
        mock_get.return_value = mock_instance
        mock_instance.is_visible_by.return_value = False
        request = utils.get_request(
            'get', '/organization/foo/', user=utils.get_anon_mock())
        assert_raises(Http404, views.organization_detail, request, 'foo')
        mock_instance.is_visible_by.assert_called_once_with(request.user)

    @patch_get_awards
    @patch_get_object
    def test_organization_request_is_successful(self, mock_get, mock_awards):
        mock_instance = Mock(spec=Organization)()
        mock_instance.interests.all.return_value = []
        mock_get.return_value = mock_instance
        mock_instance.is_visible_by.return_value = True
        mock_awards.return_value = []
        request = utils.get_request(
            'get', '/org/foo/', user=utils.get_anon_mock())
        response = views.organization_detail(request, 'foo')
        eq_(response.status_code, 200)
        eq_(response.template_name, 'organizations/object_detail.html')
        eq_(sorted(response.context_data.keys()),
            sorted(['interest_list', 'is_member', 'member_list', 'object',
                    'award_list']))


class TestOrganizationEditView(TestCase):

    def _tear_down(self):
        for model in [Organization, User]:
            model.objects.all().delete()

    def test_view_requires_authentication(self):
        request = utils.get_request(
            'get', '/org/foo/edit/', user=utils.get_anon_mock())
        response = views.organization_edit(request, 'foo')
        eq_(response.status_code, 302)
        eq_(response['Location'], utils.get_login_url('/org/foo/edit/'))

    @patch_get_object
    def test_organization_does_not_exist(self, mock_get):
        mock_get.side_effect = Http404
        request = utils.get_request(
            'get', '/org/foo/edit/', user=utils.get_user_mock())
        assert_raises(Http404, views.organization_edit, request, 'foo')
        mock_get.assert_called_once_with(
            Organization, slug__exact='foo', members=request.user)

    def test_edit_request_is_successful(self):
        user = get_user('org-user')
        organization = fixtures.get_organization(slug='foo')
        OrganizationMember.objects.create(user=user, organization=organization)
        request = utils.get_request(
            'get', '/org/foo/edit/', user=user)
        response = views.organization_edit(request, 'foo')
        eq_(response.status_code, 200)
        eq_(response.template_name, 'organizations/object_edit.html')
        eq_(sorted(response.context_data.keys()),
            ['form', 'object'])
        self._tear_down()

    def test_edit_payload_is_successful(self):
        user = get_user('org-user')
        organization = fixtures.get_organization(slug='foo')
        OrganizationMember.objects.create(user=user, organization=organization)
        data = {
            'name': 'New name',
            'bio': 'Bio',
        }
        request = utils.get_request(
            'post', '/org/foo/edit/', user=user, data=data)
        request._messages = utils.TestMessagesBackend(request)
        response = views.organization_edit(request, 'foo')
        eq_(response.status_code, 302)
        eq_(response['Location'], organization.get_absolute_url())
        org = Organization.objects.get(slug='foo')
        eq_(org.name, 'New name')
        eq_(org.bio, 'Bio')
        self._tear_down()


class TestOrganizationListTest(TestCase):

    def test_request_is_successful(self):
        request = utils.get_request(
            'get', '/org/', user=utils.get_user_mock())
        response = views.organization_list(request)
        eq_(response.status_code, 200)
        eq_(response.template_name, 'organizations/object_list.html')
        eq_(sorted(response.context_data.keys()), ['page'])
