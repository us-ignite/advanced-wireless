from nose.tools import eq_
from mock import patch

from django.test import TestCase

from us_ignite.common.tests import utils
from us_ignite.sections import views


class TestHomeView(TestCase):

    @patch('us_ignite.resources.models.Resource.published.get_homepage')
    @patch('us_ignite.hubs.models.Hub.active.get_homepage')
    @patch('us_ignite.apps.models.Application.published.get_homepage')
    def test_request_is_successful(self, app_mock, hub_mock, resource_mock):
        request = utils.get_request('get', '/')
        response = views.home(request)
        eq_(response.status_code, 200)
        eq_(response.template_name, 'home.html')
        eq_(sorted(response.context_data.keys()),
            sorted(['application', 'hub', 'resource']))
        app_mock.assert_called_once_with()
        hub_mock.assert_called_once_with()
        resource_mock.assert_called_once_with()
