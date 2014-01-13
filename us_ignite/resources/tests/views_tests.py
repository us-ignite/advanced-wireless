from nose.tools import assert_raises, eq_, ok_
from mock import Mock, patch

from django.contrib.auth.models import User
from django.http import Http404
from django.test import TestCase

from us_ignite.common.tests import utils
from us_ignite.profiles.tests.fixtures import get_user
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
        eq_(response.context_data.keys(), ['object', 'is_owner'])


class TestResourceListView(TestCase):

    @patch('us_ignite.resources.models.Resource.objects.filter')
    def test_resource_list_request_is_successful(self, mock_filter):
        mock_filter.return_value = []
        request = utils.get_request(
            'get', '/resource/', user=utils.get_anon_mock())
        response = views.resource_list(request)
        eq_(response.status_code, 200)
        eq_(response.template_name, 'resources/object_list.html')
        eq_(sorted(response.context_data.keys()), ['page'])


class TestResourceAddView(TestCase):

    def _tear_down(self):
        for model in [Resource, User]:
            model.objects.all().delete()

    def test_view_requires_authentication(self):
        request = utils.get_request(
            'get', '/resource/add/', user=utils.get_anon_mock())
        response = views.resource_add(request)
        eq_(response.status_code, 302)
        eq_(response['Location'], utils.get_login_url('/resource/add/'))

    def test_get_request_is_successful(self):
        request = utils.get_request(
            'get', '/resource/add/', user=utils.get_user_mock())
        response = views.resource_add(request)
        eq_(response.status_code, 200)
        eq_(response.template_name, 'resources/object_add.html')
        eq_(sorted(response.context_data.keys()), ['form'])

    def test_empty_post_request_fails(self):
        request = utils.get_request(
            'post', '/resource/add/', data={}, user=utils.get_user_mock())
        response = views.resource_add(request)
        eq_(response.status_code, 200)
        ok_(response.context_data['form'].errors)

    def test_post_request_succeeds(self):
        user = get_user('us-ignite')
        data = {
            'name': 'Gigabit resource',
            'description': 'Lorem Ipsum',
            'status': Resource.DRAFT,
            'url': 'http://us-ignite.org/',
        }
        request = utils.get_request(
            'post', '/resource/add/', data=data, user=user)
        response = views.resource_add(request)
        resource = Resource.objects.get(name='Gigabit resource')
        eq_(response.status_code, 302)
        eq_(response['Location'], resource.get_absolute_url())
        self._tear_down()
