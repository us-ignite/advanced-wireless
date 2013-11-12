from mock import patch
from nose.tools import eq_, ok_

from django.test import TestCase

from us_ignite.apps import aggregator


class TestRenderURL(TestCase):

    @patch('us_ignite.apps.aggregator.render_github')
    def test_github_is_rendered(self, github_mock):
        url = 'https://github.com/mozilla/mozilla-ignite'
        result = aggregator.render_url(url)
        github_mock.assert_called_once()
        ok_(result)

    @patch('us_ignite.apps.aggregator.render_twitter')
    def test_twitter_is_rendered(self, twitter_mock):
        url = 'https://twitter.com/US_Ignite'
        result = aggregator.render_url(url)
        twitter_mock.assert_called_once()
        ok_(result)

    def test_unknow_url_is_ignored(self):
        url = 'http://us-ignite.org/'
        result = aggregator.render_url(url)
        eq_(result, None)
