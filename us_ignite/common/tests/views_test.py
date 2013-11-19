from nose.tools import eq_

from django.test import client, TestCase

from us_ignite.common import views


class TestCustom404(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def test_custom_404_is_successful(self):
        request = self.factory.get('/')
        response = views.custom_404(request)
        eq_(response.status_code, 404)
        eq_(response.template_name, '404.html')


class TestCustom500(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def test_custom_404_is_successful(self):
        request = self.factory.get('/')
        response = views.custom_500(request)
        eq_(response.status_code, 500)
        eq_(response.template_name, '500.html')
