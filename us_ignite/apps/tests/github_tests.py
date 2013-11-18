from mock import patch, MagicMock
from nose.tools import eq_

from django.test import TestCase

from us_ignite.aggregator import github

patch_requests = patch('requests.get')


class TestGetCommits(TestCase):

    @patch_requests
    def test_github_response_fails_gracefully(self, mock_get):
        mock_get.side_effect = ValueError
        result = github.get_commits('madewithbytes', 'us_ignite')
        eq_(result, [])

    @patch_requests
    def test_not_ok_response_is_successfully_handled(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 405
        mock_get.return_value = mock_response
        result = github.get_commits('madewithbytes', 'us_ignite')
        eq_(result, [])

    @patch_requests
    def test_response_is_successful(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = [1] * 10
        mock_get.return_value = mock_response
        result = github.get_commits('madewithbytes', 'us_ignite')
        eq_(result, [1, 1, 1, 1, 1])

