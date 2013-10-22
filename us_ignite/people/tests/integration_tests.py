from django.contrib.auth.models import User
from django.test import TestCase

from django_nose.tools import assert_redirects
from nose.tools import eq_, ok_
from registration.models import RegistrationProfile
from us_ignite.common.tests import utils
from us_ignite.profiles.tests import fixtures


def _teardown_profiles():
    for model in [RegistrationProfile, User]:
        model.objects.all().delete()


class TestPeopleListUnauthenticated(TestCase):

    def test_people_list_is_unavailable(self):
        url = '/people/'
        response = self.client.get(url)
        assert_redirects(response, utils.get_login_url(url))


class TestPeopleListPage(TestCase):

    def setUp(self):
        self.user = fixtures.get_user(
            'us-ignite', email='user@us-ignite.org')
        self.profile = fixtures.get_profile(user=self.user)
        self.client.login(username='us-ignite', password='us-ignite')

    def tearDown(self):
        self.client.logout()
        _teardown_profiles()

    def test_get_request_is_successful(self):
        response = self.client.get('/people/')
        ok_(response.status_code, 200)
        eq_(len(response.context['page'].object_list), 1)

    def test_admin_users_are_not_listed(self):
        self.user.is_superuser = True
        self.user.save()
        response = self.client.get('/people/')
        eq_(len(response.context['page'].object_list), 0)

    def test_inactive_users_are_not_listed(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.get('/people/')
        eq_(len(response.context['page'].object_list), 0)
