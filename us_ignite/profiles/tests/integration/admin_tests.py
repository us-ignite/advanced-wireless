from datetime import datetime

from django.test import TestCase
from django.contrib.auth.models import User
from django.utils.timezone import utc

from django_nose.tools import assert_redirects
from registration.models import RegistrationProfile
from nose.tools import eq_, ok_


from us_ignite.profiles.models import Profile
from us_ignite.profiles.tests import fixtures


def _get_payload(user_list):
    users = []
    for user in user_list:
        users.append(','.join(user))
    return {'users': '\n'.join(users)}


def _teardown_profiles():
    for model in [RegistrationProfile, Profile, User]:
        model.objects.all().delete()


def assert_admin_login(response):
    eq_(response.status_code, 200)
    ok_('id_username' in response.content)
    ok_('id_password' in response.content)


class TestUnauthenticatedInviteAdmin(TestCase):

    def test_import_users_require_admin(self):
        url = '/admin/profiles/profile/inviter/'
        response = self.client.get(url)
        assert_admin_login(response)

    def test_import_post_payload_require_admin(self):
        url = '/admin/profiles/profile/inviter/'
        payload = _get_payload([('Alpha', 'alpha@us-ignite.org')])
        response = self.client.post(url, payload)
        assert_admin_login(response)


class TestRegularUserInviteAdmin(TestCase):

    def setUp(self):
        self.user = fixtures.get_user('us-ignite', email='user@us-ignite.org')
        self.client.login(username='us-ignite', password='us-ignite')

    def tearDown(self):
        self.client.logout()
        _teardown_profiles()

    def test_import_users_require_admin(self):
        url = '/admin/profiles/profile/inviter/'
        response = self.client.get(url)
        assert_admin_login(response)

    def test_import_post_payload_require_admin(self):
        url = '/admin/profiles/profile/inviter/'
        payload = _get_payload([('Alpha', 'alpha@us-ignite.org')])
        response = self.client.post(url, payload)
        assert_admin_login(response)


class TestInviteUsersAdmin(TestCase):

    def setUp(self):
        self.user = fixtures.get_user('us-ignite', email='user@us-ignite.org')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='us-ignite', password='us-ignite')

    def tearDown(self):
        self.client.logout()
        _teardown_profiles()

    def test_get_request_is_successful(self):
        url = '/admin/profiles/profile/inviter/'
        response = self.client.get(url)
        eq_(response.status_code, 200)
        ok_(response.content, 'id_users')

    def test_post_empty_payload_fails(self):
        url = '/admin/profiles/profile/inviter/'
        response = self.client.post(url, {})
        eq_(response.status_code, 200)
        ok_(response.content, 'errors')

    def test_post_valid_payload_succeds(self):
        url = '/admin/profiles/profile/inviter/'
        payload = _get_payload([('Alpha', 'alpha@us-ignite.org')])
        response = self.client.post(url, payload)
        assert_redirects(response, '/admin/profiles/profile/')
        user = User.objects.get(email='alpha@us-ignite.org')
        ok_(user.username)
        eq_(user.profile.name, 'Alpha')
        ok_(user.profile.slug)


class TestUnauthenticatedExportUsersAdmin(TestCase):

    def test_export_users_require_admin(self):
        url = '/admin/profiles/profile/export/'
        response = self.client.get(url)
        assert_admin_login(response)

    def test_export_post_payload_require_admin(self):
        url = '/admin/profiles/profile/export/'
        response = self.client.post(url, {})
        assert_admin_login(response)


class TestRegularUserExportUsersAdmin(TestCase):

    def setUp(self):
        self.user = fixtures.get_user('us-ignite', email='user@us-ignite.org')
        self.client.login(username='us-ignite', password='us-ignite')

    def tearDown(self):
        self.client.logout()
        _teardown_profiles()

    def test_export_users_require_admin(self):
        url = '/admin/profiles/profile/export/'
        response = self.client.get(url)
        assert_admin_login(response)

    def test_export_post_payload_require_admin(self):
        url = '/admin/profiles/profile/export/'
        response = self.client.post(url, {})
        assert_admin_login(response)


class TestExportUsersAdmin(TestCase):

    def setUp(self):
        self.user = fixtures.get_user('us-ignite', email='user@us-ignite.org')
        self.user.is_superuser = True
        self.user.is_staff = True
        self.user.save()
        self.client.login(username='us-ignite', password='us-ignite')

    def tearDown(self):
        self.client.logout()
        _teardown_profiles()

    def test_export_users_get_request_is_successful(self):
        url = '/admin/profiles/profile/export/'
        response = self.client.get(url)
        eq_(response.status_code, 200)
        ok_('export_users_form' in response.content)

    def test_export_shows_active_users(self):
        url = '/admin/profiles/profile/export/'
        user = fixtures.get_user(
            'john', email='no-contact@us-ignite.org', first_name='John Donne')
        fixtures.get_profile(user=user)
        response = self.client.post(url, {})
        eq_(response.status_code, 200)
        ok_('attachment;' in response['Content-Disposition'])
        eq_(response.content, 'John Donne,no-contact@us-ignite.org\r\n')

    def test_export_does_not_show_innactive_users(self):
        url = '/admin/profiles/profile/export/'
        innactive_user = fixtures.get_user(
            'paul', first_name='Paul', email='invalid@us-ignite.org',
            is_active=False)
        fixtures.get_profile(user=innactive_user)
        user = fixtures.get_user(
            'john', first_name='John Donne', email='no-contact@us-ignite.org')
        fixtures.get_profile(user=user)
        response = self.client.post(url, {})
        eq_(response.status_code, 200)
        ok_('attachment;' in response['Content-Disposition'])
        eq_(response.content, 'John Donne,no-contact@us-ignite.org\r\n')

    def test_empty_query_returns_warning(self):
        url = '/admin/profiles/profile/export/'
        response = self.client.post(url, {})
        eq_(response.status_code, 200)
        messages = [m.message for m in list(response.context['messages'])]
        eq_(messages, ['No users registered during the given dates.'])

    def test_form_filter_users_by_start_date(self):
        url = '/admin/profiles/profile/export/'
        user = fixtures.get_user('john', email='no-contact@us-ignite.org')
        created = datetime(2013, 12, 6, 0, 0, 0).replace(tzinfo=utc)
        fixtures.get_profile(user=user, name='John Donne', created=created)
        response = self.client.post(
            url, {'start_0': '2013-12-7','start_1': '00:00:00'})
        eq_(response.status_code, 200)
        messages = [m.message for m in list(response.context['messages'])]
        eq_(messages, ['No users registered during the given dates.'])

    def test_form_filter_users_by_end_date(self):
        url = '/admin/profiles/profile/export/'
        user = fixtures.get_user('john', email='no-contact@us-ignite.org')
        created = datetime(2013, 12, 6, 0, 0, 0).replace(tzinfo=utc)
        fixtures.get_profile(user=user, name='John Donne', created=created)
        response = self.client.post(
            url, {'end_0': '2013-12-5', 'end_1': '00:00:00'})
        eq_(response.status_code, 200)
        messages = [m.message for m in list(response.context['messages'])]
        eq_(messages, ['No users registered during the given dates.'])

    def test_form_filter_uses_end_and_start_date(self):
        url = '/admin/profiles/profile/export/'
        user = fixtures.get_user(
            'john', email='no-contact@us-ignite.org', first_name='John Donne')
        created = datetime(2013, 12, 6).replace(tzinfo=utc)
        fixtures.get_profile(user=user,  created=created)
        response = self.client.post(url, {
            'start_0': '2013-12-5',
            'start_1': '00:00:00',
            'end_0': '2013-12-7',
            'end_1': '23:59:59',
        })
        eq_(response.status_code, 200)
        eq_(response.status_code, 200)
        ok_('attachment;' in response['Content-Disposition'])
        eq_(response.content, 'John Donne,no-contact@us-ignite.org\r\n')
