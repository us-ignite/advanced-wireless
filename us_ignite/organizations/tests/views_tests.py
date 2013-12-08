from nose.tools import assert_raises, eq_
from mock import patch, Mock

from django.http import Http404
from django.test import TestCase

from us_ignite.common.tests import utils
from us_ignite.organizations import views
from us_ignite.organizations.models import Organization

patch_get_object = patch('us_ignite.organizations.views.get_object_or_404')


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

    @patch_get_object
    def test_organization_request_is_successful(self, mock_get):
        mock_instance = Mock(spec=Organization)()
        mock_get.return_value = mock_instance
        mock_instance.is_visible_by.return_value = True
        request = utils.get_request(
            'get', '/organization/foo/', user=utils.get_anon_mock())
        response = views.organization_detail(request, 'foo')
        eq_(response.status_code, 200)
        eq_(response.template_name, 'organizations/object_detail.html')
        eq_(sorted(response.context_data.keys()), ['member_list', 'object'])
