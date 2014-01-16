from mock import patch
from nose.tools import eq_

from django.test import TestCase

from us_ignite.apps.models import Application
from us_ignite.common.tests import utils
from us_ignite.events.models import Event
from us_ignite.hubs.models import Hub
from us_ignite.organizations.models import Organization
from us_ignite.search import views


patch_search = patch('us_ignite.search.views.tag_search')


class TestSearchAppsView(TestCase):

    @patch_search
    def test_search_tag_is_successful(self, search_mock):
        search_mock.return_value = 'ok'
        request = utils.get_request('get', '/search/apps/')
        response = views.search_apps(request)
        eq_(response, 'ok')
        search_mock.assert_called_once_with(
            request, Application.active, 'search/application_list.html')


class TestSearchEventsView(TestCase):

    @patch_search
    def test_search_tag_is_successful(self, search_mock):
        search_mock.return_value = 'ok'
        request = utils.get_request('get', '/search/events/')
        response = views.search_events(request)
        eq_(response, 'ok')
        search_mock.assert_called_once_with(
            request, Event.published, 'search/event_list.html')


class TestHubEventsView(TestCase):

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
