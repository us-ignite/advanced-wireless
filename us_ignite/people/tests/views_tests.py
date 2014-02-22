from mock import Mock, patch
from nose.tools import eq_, ok_

from django.contrib.auth.models import User
from django.test import client, TestCase

from us_ignite.apps.models import Application
from us_ignite.common.tests import utils
from us_ignite.events.models import Event
from us_ignite.hubs.models import Hub, HubMembership
from us_ignite.organizations.models import Organization, OrganizationMember
from us_ignite.profiles.tests import fixtures
from us_ignite.people import views
from us_ignite.resources.models import Resource


def _teardown_profiles():
    for model in [User]:
        model.objects.all().delete()


class TestProfileListView(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def _get_request(self, url='/people/', data=None):
        data = data if data else {}
        request = self.factory.get(url, data)
        request.user = utils.get_user_mock()
        return request

    def test_profile_list_requires_authentication(self):
        request = self.factory.get('/people/')
        request.user = utils.get_anon_mock()
        response = views.profile_list(request)
        eq_(response.status_code, 302)
        eq_(response['Location'], utils.get_login_url('/people/'))

    def test_authenticated_profile_list_is_successful(self):
        request = self._get_request()
        response = views.profile_list(request)
        eq_(response.status_code, 200)
        eq_(len(response.context_data['page'].object_list), 0)

    def test_authenticated_profile_list_context(self):
        response = views.profile_list(self._get_request())
        eq_(response.status_code, 200)
        eq_(sorted(response.context_data.keys()),
            ['order', 'order_form', 'page'])

    def test_admin_users_are_listed(self):
        user = fixtures.get_user('us-ignite', is_superuser=True)
        fixtures.get_profile(user=user, name='us ignite')
        response = views.profile_list(self._get_request())
        eq_(response.status_code, 200)
        eq_(len(response.context_data['page'].object_list), 1)
        _teardown_profiles()

    def test_inactive_users_are_not_listed(self):
        user = fixtures.get_user('us-ignite', is_active=False)
        fixtures.get_profile(user=user, name='us ignite')
        response = views.profile_list(self._get_request())
        eq_(response.status_code, 200)
        eq_(len(response.context_data['page'].object_list), 0)
        _teardown_profiles()

    def test_users_can_be_sorted(self):
        user_a = fixtures.get_user('alpha')
        profile_a = fixtures.get_profile(user=user_a, name='alpha')
        user_b = fixtures.get_user('beta')
        profile_b = fixtures.get_profile(user=user_b, name='beta')
        request = self._get_request(data={'order': 'name'})
        response = views.profile_list(request)
        eq_(list(response.context_data['page'].object_list),
            [profile_a, profile_b])
        _teardown_profiles()

    def test_users_can_be_reverse_sorted(self):
        user_a = fixtures.get_user('alpha')
        profile_a = fixtures.get_profile(user=user_a, name='alpha')
        user_b = fixtures.get_user('beta')
        profile_b = fixtures.get_profile(user=user_b, name='beta')
        request = self._get_request(data={'order': '-name'})
        response = views.profile_list(request)
        eq_(list(response.context_data['page'].object_list),
            [profile_b, profile_a])
        _teardown_profiles()


class TestProfileDetailView(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def _get_request(self, url='/people/someone/', data=None):
        data = data if data else {}
        request = self.factory.get(url, data)
        request.user = utils.get_user_mock()
        return request

    def test_profile_detail_requires_authentication(self):
        request = self.factory.get('/people/someone/')
        request.user = utils.get_anon_mock()
        response = views.profile_detail(request)
        eq_(response.status_code, 302)
        eq_(response['Location'], utils.get_login_url('/people/someone/'))

    def test_superuser_profile_is_available(self):
        user = fixtures.get_user('us-ignite', is_superuser=True)
        fixtures.get_profile(user=user, slug='someone', name='us ignite')
        request = self._get_request()
        response = views.profile_detail(request, 'someone')
        ok_(response.status_code, 200)
        eq_(sorted(response.context_data.keys()),
            sorted(['object', 'application_list', 'event_list',
                    'resource_list', 'hub_membership_list', 'hub_list',
                    'hub_request_list', 'organization_list', 'award_list',
                    'is_owner']))
        _teardown_profiles()

    def test_get_request_is_successful(self):
        user = fixtures.get_user('us-ignite')
        fixtures.get_profile(user=user, slug='someone', name='us ignite')
        response = views.profile_detail(self._get_request(), 'someone')
        ok_(response.status_code, 200)
        eq_(sorted(response.context_data.keys()),
            sorted(['object', 'application_list', 'event_list',
                    'resource_list', 'hub_membership_list', 'hub_list',
                    'hub_request_list', 'organization_list', 'award_list',
                    'is_owner']))
        _teardown_profiles()


patch_application_filter = patch(
    'us_ignite.apps.models.Application.active.filter',
    return_value=Application.objects.none())


class TestGetApplicationListFunction(TestCase):

    @patch_application_filter
    def test_empty_viewer_returns_public_apps(self, filter_mock):
        owner = utils.get_user_mock()
        result = views.get_application_list(owner)
        filter_mock.assert_called_once_with(
            owner=owner, status=Application.PUBLISHED)
        eq_(list(result), [])

    @patch_application_filter
    def test_different_viewer_returns_public_apps(self, filter_mock):
        owner = utils.get_user_mock()
        viewer = utils.get_user_mock()
        result = views.get_application_list(owner, viewer=viewer)
        filter_mock.assert_called_once_with(
            owner=owner, status=Application.PUBLISHED)
        eq_(list(result), [])

    @patch_application_filter
    def test_owner_viewer_returns_all_apps(self, filter_mock):
        owner = utils.get_user_mock()
        result = views.get_application_list(owner, viewer=owner)
        filter_mock.assert_called_once_with(owner=owner)
        eq_(list(result), [])


patch_event_filter = patch(
    'us_ignite.events.models.Event.objects.filter',
    return_value=Event.objects.none()
)


class TestEventListFunction(TestCase):

    @patch_event_filter
    def test_anon_user_returns_public_objects(self, filter_mock):
        user = utils.get_user_mock()
        viewer = utils.get_anon_mock()
        result = views.get_event_list(user, viewer=viewer)
        filter_mock.assert_called_once_with(user=user, status=Event.PUBLISHED)
        eq_(list(result), [])

    @patch_event_filter
    def test_owner_returns_all_available_objects(self, filter_mock):
        user = utils.get_user_mock()
        result = views.get_event_list(user, viewer=user)
        filter_mock.assert_called_once_with(user=user)
        eq_(list(result), [])


patch_resource_filter = patch(
    'us_ignite.resources.models.Resource.objects.filter',
    return_value=Resource.objects.none()
)


class TestResourceListFunction(TestCase):

    @patch_resource_filter
    def test_anon_user_returns_public_objects(self, filter_mock):
        contact = utils.get_user_mock()
        viewer = utils.get_anon_mock()
        result = views.get_resource_list(contact, viewer=viewer)
        filter_mock.assert_called_once_with(
            contact=contact, status=Resource.PUBLISHED)
        eq_(list(result), [])

    @patch_resource_filter
    def test_contact_returns_all_available_objects(self, filter_mock):
        contact = utils.get_user_mock()
        result = views.get_resource_list(contact, viewer=contact)
        filter_mock.assert_called_once_with(contact=contact)
        eq_(list(result), [])


patch_hub_filter = patch(
    'us_ignite.hubs.models.Hub.objects.filter',
    return_value=Hub.objects.none()
)


class TestHubListFunction(TestCase):

    @patch_hub_filter
    def test_anon_user_returns_public_objects(self, filter_mock):
        guardian = utils.get_user_mock()
        viewer = utils.get_anon_mock()
        result = views.get_hub_list(guardian, viewer=viewer)
        filter_mock.assert_called_once_with(guardian=guardian, status=Hub.PUBLISHED)
        eq_(list(result), [])

    @patch_hub_filter
    def test_owner_returns_all_available_objects(self, filter_mock):
        guardian = utils.get_user_mock()
        result = views.get_hub_list(guardian, viewer=guardian)
        filter_mock.assert_called_once_with(guardian=guardian)
        eq_(list(result), [])


patch_organization_related = patch(
    'us_ignite.organizations.models.OrganizationMember.objects.select_related')


class TestOrganizationListFunction(TestCase):

    @patch_organization_related
    def test_anon_user_returns_public_objects(self, related_mock):
        filter_mock = Mock()
        filter_mock.filter.return_value = OrganizationMember.objects.none()
        related_mock.return_value = filter_mock
        user = utils.get_user_mock()
        viewer = utils.get_anon_mock()
        result = views.get_organization_list(user, viewer=viewer)
        related_mock.assert_called_once_with('organization')
        filter_mock.filter.assert_called_once_with(
            user=user, organization__status=Organization.PUBLISHED)

    @patch_organization_related
    def test_owner_returns_all_available_objects(self, related_mock):
        filter_mock = Mock()
        filter_mock.filter.return_value = OrganizationMember.objects.none()
        related_mock.return_value = filter_mock
        user = utils.get_user_mock()
        result = views.get_organization_list(user, viewer=user)
        related_mock.assert_called_once_with('organization')
        filter_mock.filter.assert_called_once_with(user=user)


patch_hub_membership_related = patch(
    'us_ignite.hubs.models.HubMembership.objects.select_related')


class TestHubMembershipListFunction(TestCase):

    @patch_hub_membership_related
    def test_anon_user_returns_public_objects(self, related_mock):
        filter_mock = Mock()
        filter_mock.filter.return_value = HubMembership.objects.none()
        related_mock.return_value = filter_mock
        user = utils.get_user_mock()
        viewer = utils.get_anon_mock()
        result = views.get_hub_membership_list(user, viewer=viewer)
        related_mock.assert_called_once_with('hub')
        filter_mock.filter.assert_called_once_with(
            user=user, hub__status=Hub.PUBLISHED)

    @patch_hub_membership_related
    def test_owner_returns_all_available_objects(self, related_mock):
        filter_mock = Mock()
        filter_mock.filter.return_value = HubMembership.objects.none()
        related_mock.return_value = filter_mock
        user = utils.get_user_mock()
        result = views.get_hub_membership_list(user, viewer=user)
        related_mock.assert_called_once_with('hub')
        filter_mock.filter.assert_called_once_with(user=user)


patch_award_related = patch(
    'us_ignite.awards.models.UserAward.objects.select_related')


class TestAwardListFunction(TestCase):

    @patch_award_related
    def test_awards_are_returned(self, mock_related):
        mock_related.return_value.filter.return_value = []
        user = utils.get_user_mock()
        result = views.get_award_list(user)
        eq_(result, [])
        mock_related.assert_called_once_with('award')
        mock_related.return_value.filter.assert_called_once_with(user=user)
