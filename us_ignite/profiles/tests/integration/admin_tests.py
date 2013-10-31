from django.test import TestCase
from django.contrib.auth.models import User

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
        eq_(user.profile.display_name, 'Alpha')
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
        user = fixtures.get_user('john', email='no-contact@us-ignite.org')
        fixtures.get_profile(user=user, display_name='John Donne')
        response = self.client.post(url, {})
        eq_(response.status_code, 200)
        ok_('attachment;' in response['Content-Disposition'])
        eq_(response.content, 'John Donne,no-contact@us-ignite.org\r\n')

    def test_export_does_not_show_innactive_users(self):
        url = '/admin/profiles/profile/export/'
        user = fixtures.get_user(
            'john', email='no-contact@us-ignite.org')
        user.is_active = False
        user.save()
        fixtures.get_profile(user=user, display_name='John Donne')
        response = self.client.post(url, {})
        eq_(response.status_code, 200)
        ok_('attachment;' in response['Content-Disposition'])
        eq_(response.content, '')

