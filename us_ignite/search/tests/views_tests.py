from mock import patch
from nose.tools import eq_

from django.test import TestCase

from us_ignite.common.tests import utils
from us_ignite.events.models import Event
from us_ignite.hubs.models import Hub
from us_ignite.organizations.models import Organization
from us_ignite.resources.models import Resource
from us_ignite.search import views

from taggit.models import Tag


patch_search = patch('us_ignite.search.views.tag_search')


class TestSearchAppsView(TestCase):

    @patch('us_ignite.apps.models.Application.active.filter')
    @patch_search
    def test_search_tag_is_successful(self, search_mock, mock_filter):
        mock_filter.return_value = []
        search_mock.return_value = 'ok'
        request = utils.get_request('get', '/search/apps/')
        response = views.search_apps(request)
        eq_(response, 'ok')
        search_mock.assert_called_once_with(
            request, [], 'search/application_list.html')


class TestSearchEventsView(TestCase):

    @patch_search
    def test_search_tag_is_successful(self, search_mock):
        search_mock.return_value = 'ok'
        request = utils.get_request('get', '/search/events/')
        response = views.search_events(request)
        eq_(response, 'ok')
        search_mock.assert_called_once_with(
            request, Event.published, 'search/event_list.html')


class TestHubsView(TestCase):

    @patch_search
    def test_search_tag_is_successful(self, search_mock):
        search_mock.return_value = 'ok'
        request = utils.get_request('get', '/search/hubs/')
        response = views.search_hubs(request)
        eq_(response, 'ok')
        search_mock.assert_called_once_with(
            request, Hub.active, 'search/hub_list.html')


class TestSearchOrganizationView(TestCase):

    @patch_search
    def test_search_tag_is_successful(self, search_mock):
        search_mock.return_value = 'ok'
        request = utils.get_request('get', '/search/orgs/')
        response = views.search_organizations(request)
        eq_(response, 'ok')
        search_mock.assert_called_once_with(
            request, Organization.active, 'search/organization_list.html')


class TestSearchResourceView(TestCase):

    @patch_search
    def test_search_tag_is_successful(self, search_mock):
        search_mock.return_value = 'ok'
        request = utils.get_request('get', '/search/resource/')
        response = views.search_resources(request)
        eq_(response, 'ok')
        search_mock.assert_called_once_with(
            request, Resource.published, 'search/resource_list.html')


class TestSearchView(TestCase):

    @patch('watson.search')
    def test_get_queryless_request_is_successful(self, mock_watson):
        request = utils.get_request('get', '/search/')
        response = views.search(request)
        eq_(response.status_code, 200)
        eq_(response.template_name, 'search/object_list.html')
        eq_(sorted(response.context_data.keys()),
            ['form', 'page', 'pagination_qs'])
        eq_(response.context_data['page'].object_list, [])
        eq_(response.context_data['pagination_qs'], '')
        eq_(mock_watson.call_count, 0)

    @patch('watson.search')
    def test_query_request_is_successful(self, mock_watson):
        mock_watson.return_value = []
        request = utils.get_request('get', '/search/', data={'q': 'gigabit'})
        response = views.search(request)
        eq_(response.status_code, 200)
        eq_(response.template_name, 'search/object_list.html')
        eq_(sorted(response.context_data.keys()),
            ['form', 'page', 'pagination_qs'])
        eq_(response.context_data['page'].object_list, [])
        eq_(response.context_data['pagination_qs'], '&q=gigabit')
        mock_watson.assert_called_once_with('gigabit')


class TestTagListView(TestCase):

    @patch('taggit.models.Tag.objects.filter')
    def test_tag_list_is_successful(self, mock_filter):
        mock_filter.return_value = Tag.objects.none()
        request = utils.get_request('get', '/search/tags.json')
        response = views.tag_list(request)
        eq_(response.status_code, 200)
        eq_(response['Content-Type'], 'application/javascript')
        eq_(response.content, u"[]")
        mock_filter.assert_called_once_with(is_featured=True)
