from mock import patch
from nose.tools import eq_, ok_

from django.db.models import Q
from django.test import TestCase

from us_ignite.common.tests import utils
from us_ignite.hubs import models, views


patch_hub_request_filter = patch(
    'us_ignite.hubs.models.HubRequest.objects.filter')
patch_hub_request_form_save = patch(
    'us_ignite.hubs.forms.HubRequestForm.save')


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
    @patch_hub_request_form_save
    def test_submission_is_successful(self, mock_save, *args):
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

