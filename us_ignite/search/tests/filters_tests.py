from mock import Mock, patch
from nose.tools import eq_

from django.db.models import Model
from django.test import TestCase

from us_ignite.search import filters
from us_ignite.common.tests import utils


qs_patch = patch('us_ignite.search.filters.get_queryset')


class TestTagSearchView(TestCase):

    @qs_patch
    def test_tag_search_has_no_query(self, qs_mock):
        request = utils.get_request('get', '/search/apps/')
        response = filters.tag_search(
            request, Model, template='tag_list.html')
        eq_(response.status_code, 200)
        eq_(response.template_name, 'tag_list.html')
        eq_(sorted(response.context_data.keys()), ['form', 'page'])
        eq_(qs_mock.call_count, 0)

    @qs_patch
    def test_search_tags_search(self, qs_mock):
        qs_instance = Mock()
        qs_instance.filter.return_value = []
        qs_mock.return_value = qs_instance
        data = {'tag': 'test'}
        request = utils.get_request('get', '/search/apps/', data=data)
        response = filters.tag_search(
            request, Model, template='tag_list.html')
        qs_mock.assert_called_once_with(Model)
        qs_instance.filter.assert_called_once_with(tags__name='test')
        eq_(response.status_code, 200)
        eq_(response.template_name, 'tag_list.html')
        eq_(sorted(response.context_data.keys()), ['form', 'page'])
