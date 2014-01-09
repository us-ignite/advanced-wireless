from nose.tools import assert_raises, eq_, ok_
from mock import Mock, patch

from django.http import Http404
from django.test import TestCase

from us_ignite.common.tests import utils
from us_ignite.resources.models import Resource
from us_ignite.resources import views

patch_get = patch('us_ignite.resources.views.get_object_or_404')


class TestResourceDetailView(TestCase):

    @patch_get
    def test_invalid_resource_request_raises_404(self, mock_get):
        mock_get.side_effect = Http404
        request = utils.get_request(
            'get', '/resource/foo/', user=utils.get_anon_mock())
        assert_raises(Http404, views.resource_detail, request, 'foo')
        mock_get.assert_called_once_with(Resource, slug__exact='foo')

    @patch_get
    def test_non_visible_resource_raises_404(self, mock_get):
        instance_mock = Mock(spec=Resource)
        instance_mock.is_visible_by.return_value = False
        mock_get.return_value = instance_mock
        request = utils.get_request(
            'get', '/resource/foo/', user=utils.get_anon_mock())
        assert_raises(Http404, views.resource_detail, request, 'foo')
        mock_get.assert_called_once_with(Resource, slug__exact='foo')
        instance_mock.is_visible_by.assert_called_once_with(request.user)

    @patch_get
    def test_resource_request_is_successful(self, mock_get):
        instance_mock = Mock(spec=Resource)
        instance_mock.is_visible_by.return_value = True
        mock_get.return_value = instance_mock
        request = utils.get_request(
            'get', '/resource/foo/', user=utils.get_anon_mock())
        response = views.resource_detail(request, 'foo')
        eq_(response.status_code, 200)
        eq_(response.template_name, 'resources/object_detail.html')
        eq_(response.context_data.keys(), ['object'])


class TestResourceListView(TestCase):

    @patch('us_ignite.resources.models.Resource.objects.filter')
    def test_resource_list_request_is_successful(self, mock_filter):
        mock_filter.return_value = []
        request = utils.get_request(
            'get', '/events/', user=utils.get_anon_mock())
        response = views.resource_list(request)
        eq_(response.status_code, 200)
        eq_(response.template_name, 'resources/object_list.html')
        eq_(sorted(response.context_data.keys()), ['page'])
