from nose.tools import eq_

from django.contrib.auth.models import User
from django.test import client, TestCase

from us_ignite.apps import views
from us_ignite.apps. models import Application
from us_ignite.apps.tests import fixtures
from us_ignite.profiles.tests.fixtures import get_user


def _teardown_apps():
    for model in [User, Application]:
        model.objects.all().delete()


class TestAppListView(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def test_application_context_is_valid(self):
        response = views.app_list(self.factory.get('/app/'))
        eq_(sorted(response.context_data.keys()),
            ['order', 'order_form', 'page'])

    def test_non_published_applications_are_not_shown(self):
        fixtures.get_application(
            name='Gigabit app', status=Application.DRAFT)
        response = views.app_list(self.factory.get('/app/'))
        eq_(response.status_code, 200)
        eq_(len(response.context_data['page'].object_list), 0)
        _teardown_apps()

    def test_published_applications_are_listed(self):
        app = fixtures.get_application(
            name='Gigabit app', status=Application.PUBLISHED)
        response = views.app_list(self.factory.get('/app/'))
        eq_(response.status_code, 200)
        eq_(list(response.context_data['page'].object_list), [app])
        _teardown_apps()

    def test_applications_are_sorted(self):
        owner = get_user('us-ignite')
        app_a = fixtures.get_application(
            name='alpha app', status=Application.PUBLISHED, owner=owner)
        app_b = fixtures.get_application(
            name='beta app', status=Application.PUBLISHED, owner=owner)
        response = views.app_list(self.factory.get('/app/', {'order': 'name'}))
        eq_(list(response.context_data['page'].object_list), [app_a, app_b])
        _teardown_apps()

    def test_applications_are_reverse_sorted(self):
        owner = get_user('us-ignite')
        app_a = fixtures.get_application(
            name='alpha app', status=Application.PUBLISHED, owner=owner)
        app_b = fixtures.get_application(
            name='beta app', status=Application.PUBLISHED, owner=owner)
        response = views.app_list(self.factory.get('/app/', {'order': '-name'}))
        eq_(list(response.context_data['page'].object_list), [app_b, app_a])
        _teardown_apps()
