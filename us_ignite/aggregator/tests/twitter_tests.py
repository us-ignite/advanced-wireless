import twython

from mock import call, patch, Mock
from nose.tools import eq_

from django.conf import settings
from django.test import TestCase
from django.test.utils import override_settings


from us_ignite.aggregator import twitter


patch_twython = patch('twython.Twython')


class TestGetTimeline(TestCase):

    @patch_twython
    @override_settings(TWITTER_API_KEY='', TWITTER_API_SECRET='')
    def test_missing_settings_bailout_timeline(self, mock_twython):
        timeline = twitter.get_timeline('us_ignite')
        eq_(timeline, [])

    @patch_twython
    @patch('us_ignite.aggregator.twitter._get_access_token')
    def test_timeline_is_successful(self, mock_token, mock_twython):
        mock_token.return_value = 'access_token'
        mock_instance = Mock(spec=twython.Twython)()
        mock_instance.get_user_timeline.return_value = [1] * 10
        mock_twython.return_value = mock_instance
        timeline = twitter.get_timeline('us_ignite')
        mock_token.assert_called_once()
        mock_twython.assert_called_once_with(
            settings.TWITTER_API_KEY, access_token='access_token')
        eq_(timeline, [1, 1, 1, 1, 1])
