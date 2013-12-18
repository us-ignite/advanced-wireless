from nose.tools import eq_

from django.test import TestCase, client

from us_ignite.common import middleware


class TestDoNotTrackMiddleware(TestCase):

    def setUp(self):
        self.factory = client.RequestFactory()

    def test_request_is_set_to_dnt(self):
        request = self.factory.get('/')
        request.META['HTTP_DNT'] = '1'
        instance = middleware.DoNotTrackMiddleware()
        instance.process_request(request)
        eq_(request.is_dnt, True)

    def test_request_does_not_contain_dnt_header(self):
        request = self.factory.get('/')
        instance = middleware.DoNotTrackMiddleware()
        instance.process_request(request)
        eq_(request.is_dnt, False)

    def test_request_contains_invalid_value(self):
        request = self.factory.get('/')
        request.META['HTTP_DNT'] = 'INVALID'
        instance = middleware.DoNotTrackMiddleware()
        instance.process_request(request)
        eq_(request.is_dnt, False)
