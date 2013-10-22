from django.test import TestCase

from nose.tools import eq_
from us_ignite.common import pagination


class TestGetPageNumber(TestCase):

    def test_invalid_number_returns_default(self):
        request_get = {'page': 'INVALID'}
        page = pagination.get_page_no(request_get)
        eq_(page, 1)

    def test_empty_get_request_returns_default(self):
        request_get = {}
        page = pagination.get_page_no(request_get)
        eq_(page, 1)

    def test_valid_integer_is_returned(self):
        request_get = {'page': '34'}
        page = pagination.get_page_no(request_get)
        eq_(page, 34)

    def test_negative_integer_returns_default(self):
        request_get = {'page': '-11'}
        page = pagination.get_page_no(request_get)
        eq_(page, 1)


class TestGetPagePaginator(TestCase):

    def test_empty_page_returns_first_page(self):
        object_list = [2] * 22
        page = pagination.get_page(object_list, 22)
        eq_(page.number, 1)

    def test_existing_page_returns_correctly(self):
        object_list = [2] * 33
        page = pagination.get_page(object_list, 2)
        eq_(page.number, 2)

    def test_negative_page_returns_first_page(self):
        object_list = [2] * 44
        page = pagination.get_page(object_list, -1)
        eq_(page.number, 1)

