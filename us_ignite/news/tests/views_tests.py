from mock import patch
from nose.tools import eq_

from django.test import TestCase

from us_ignite.common.tests import utils
from us_ignite.news import views, models


class TestArticleListView(TestCase):

    @patch('us_ignite.news.models.Article.published.filter')
    def test_article_list_request_is_successful(self, mock_all):
        mock_all.return_value = []
        request = utils.get_request('get', '/news/')
        response = views.article_list(request)
        eq_(response.status_code, 200)
        eq_(response.template_name, 'news/object_list.html')
        eq_(sorted(response.context_data.keys()), ['page'])
        mock_all.assert_called_once_with(section=models.Article.DEFAULT)
