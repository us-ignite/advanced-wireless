from mock import patch
from nose.tools import eq_

from django.db.models import Model
from django.test import TestCase

from us_ignite.search import filters
from us_ignite.common.tests import utils


qs_patch = patch('watson.search')
get_qs_patch = patch('us_ignite.search.filters.get_queryset')


class TestTagSearchView(TestCase):

    @get_qs_patch
    def test_tag_search_has_no_url_query(self, get_qs_mock):
        get_qs_mock.return_value = []
        request = utils.get_request('get', '/search/apps/')
        response = filters.tag_search(
            request, Model, template='tag_list.html')
        eq_(response.status_code, 200)
        eq_(response.template_name, 'tag_list.html')
        eq_(sorted(response.context_data.keys()),
            sorted(['form', 'page', 'pagination_qs']))
        eq_(get_qs_mock.call_count, 0)

    @qs_patch
    @get_qs_patch
    def test_search_tags_search(self, get_qs_mock, qs_mock):
        get_qs_mock.return_value = []
        qs_mock.return_value = []
        data = {'q': 'test'}
        request = utils.get_request('get', '/search/apps/', data=data)
        response = filters.tag_search(
            request, Model, template='tag_list.html')
        get_qs_mock.assert_called_once_with(Model)
        qs_mock.assert_called_once_with('test', models=([], ))
        eq_(response.status_code, 200)
        eq_(response.template_name, 'tag_list.html')
        eq_(sorted(response.context_data.keys()),
            sorted(['form', 'page', 'pagination_qs']))
