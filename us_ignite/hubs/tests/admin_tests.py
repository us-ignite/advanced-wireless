from nose.tools import raises, eq_, ok_
from mock import patch, Mock

from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from django.http import Http404
from django.test import client, TestCase

from us_ignite.common.tests import utils
from us_ignite.hubs.admin import HubRequestAdmin, get_hub_from_request
from us_ignite.hubs.models import HubRequest, Hub
from us_ignite.hubs.tests import fixtures


patch_request_get = patch('us_ignite.hubs.models.HubRequest.objects.get')


class HubRequestAdminTest(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()
        self.site = AdminSite()

    def _tear_down(self):
        for model in [HubRequest, Hub]:
            model.objects.all().delete()

    @raises(Http404)
    def test_approve_request_does_not_exists_fails(self):
        admin = HubRequestAdmin(HubRequest, self.site)
        request = self.factory.get('/')
        admin.approve_request(request, 1)

    @raises(Http404)
    @patch_request_get
    def test_request_has_been_approved_fails(self, mock_get):
        mock_instance = Mock(spec=HubRequest)()
        mock_instance.is_pending.return_value = False
        mock_get.return_value = mock_instance
        admin = HubRequestAdmin(HubRequest, self.site)
        request = self.factory.get('/')
        admin.approve_request(request, 1)

    @patch_request_get
    @patch('us_ignite.hubs.admin.HubApprovalRequestForm')
    def test_request_admin_is_render_successfully(self, mock_form, mock_get):
        mock_instance = Mock(spec=HubRequest)()
        mock_instance.is_pending.return_value = True
        mock_get.return_value = mock_instance
        admin = HubRequestAdmin(HubRequest, self.site)
        request = self.factory.get('/')
        response = admin.approve_request(request, 1)
        mock_get.assert_called_once_with(id=1)
        mock_form.assert_called_once()
        eq_(response.status_code, 200)
        eq_(response.template_name, 'admin/hubs/request_approval.html')
        eq_(sorted(response.context_data.keys()),
            sorted(['object', 'form', 'title']))

    def test_request_admin_is_approved(self):
        hub_request = fixtures.get_hub_request()
        admin = HubRequestAdmin(HubRequest, self.site)
        request = self.factory.post('/', {'status': HubRequest.APPROVED})
        request._messages = utils.TestMessagesBackend(request)
        response = admin.approve_request(request, hub_request.id)
        eq_(response.status_code, 302)
        eq_(response['Location'],
            '/admin/hubs/hubrequest/%s/' % hub_request.id)
        instance = HubRequest.objects.get(id=hub_request.id)
        ok_(instance.hub)
        self._tear_down()


class TestGetHubFromRequestAdmin(TestCase):

    @patch('us_ignite.hubs.models.Hub.objects.create')
    def test_creation_is_successful(self, mock_create):
        user = User(id=1)
        data = {
            'name': 'Hello',
            'user': user,
            'summary': 'Summary',
            'description': 'Description',
            'website': 'http://us-ignite.org',
        }
        instance = HubRequest(**data)
        get_hub_from_request(instance)
        mock_create.assert_called_once_with(
            name='Hello',
            contact=user,
            summary='Summary',
            description='Description',
            website='http://us-ignite.org'
        )
