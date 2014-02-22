from nose.tools import eq_

from django.contrib.auth.models import User
from django.test import TestCase

from django_nose.tools import assert_redirects
from us_ignite.common.tests import utils
from us_ignite.profiles.tests import fixtures


def _teardown_profiles():
    for model in [User]:
        model.objects.all().delete()


class TestPeopleListUnauthenticated(TestCase):

    def test_people_list_requires_auth(self):
        url = '/people/'
        response = self.client.get(url)
        assert_redirects(response, utils.get_login_url(url))

    def test_people_list_is_successful(self):
        user = fixtures.get_user('us-ignite')
        fixtures.get_profile(user=user, name='us ignite', slug='ignite')
        self.client.login(username='us-ignite', password='us-ignite')
        response = self.client.get('/people/')
        eq_(response.status_code, 200)
        self.client.logout()
        _teardown_profiles()


class TestPeopleDetailPage(TestCase):

    def test_people_page_detail_is_successful(self):
        user = fixtures.get_user('us-ignite')
        fixtures.get_profile(user=user, name='us ignite', slug='ignite')
        self.client.login(username='us-ignite', password='us-ignite')
        response = self.client.get('/people/ignite/')
        eq_(response.status_code, 200)
        self.client.logout()
        _teardown_profiles()

    def test_people_page_detail_requires_auth(self):
        user = fixtures.get_user('us-ignite')
        fixtures.get_profile(user=user, name='us ignite', slug='ignite')
        response = self.client.get('/people/ignite/')
        assert_redirects(response, utils.get_login_url('/people/ignite/'))
        _teardown_profiles()
