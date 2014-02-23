from nose.tools import eq_

from django.test import TestCase

from us_ignite.common.response import json_response


class TestJSONResponseFunction(TestCase):

    def test_response_without_callback_is_valid(self):
        data = {'hello': 'world'}
        response = json_response(data)
        eq_(response.status_code, 200)
        eq_(response.content, u'{"hello": "world"}')
        eq_(response['Content-Type'], 'application/javascript')

    def test_response_with_callback_is_valid(self):
        data = {'hello': 'world'}
        response = json_response(data, callback='foo')
        eq_(response.status_code, 200)
        eq_(response.content, u'foo({"hello": "world"})')
        eq_(response['Content-Type'], 'application/javascript')
