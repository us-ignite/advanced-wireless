from mock import patch
from nose.tools import eq_, ok_

from django.test import TestCase

from us_ignite.aggregator import renderer


class TestRenderURL(TestCase):

    @patch('us_ignite.aggregator.renderer.SUPPORTED_URLS')
    def test_github_is_rendered(self, urls_mock):
        url = 'https://github.com/mozilla/mozilla-ignite'
        renderer.render_url(url)
        urls_mock.get.assert_called_once_with('github.com')


    @patch('us_ignite.aggregator.renderer.SUPPORTED_URLS')
    def test_twitter_is_rendered(self, urls_mock):
        url = 'https://twitter.com/US_Ignite'
        renderer.render_url(url)
        urls_mock.get.assert_called_once_with('twitter.com')

    @patch('us_ignite.aggregator.renderer.SUPPORTED_URLS')
    def test_unknow_url_is_ignored(self, urls_mock):
        urls_mock.get.return_value = None
        url = 'http://us-ignite.org/'
        result = renderer.render_url(url)
        urls_mock.get.assert_called_once_with('us-ignite.org')
        eq_(result, None)
