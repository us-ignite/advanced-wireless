from mock import patch, MagicMock
from nose.tools import eq_

from django.test import TestCase

from us_ignite.aggregator import github

patch_requests = patch('requests.get')


def _get_commit_response(extra_data=None):
    data = {
        'commit': {
            'message': 'Hello!',
        }
    }
    if extra_data:
        data.update(extra_data)
    return data


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
        mock_response.json.return_value = [_get_commit_response()] * 10
        mock_get.return_value = mock_response
        result = github.get_commits('madewithbytes', 'us_ignite')
        extra_data = {'cleaned_commit': 'Hello!'}
        eq_(result, [_get_commit_response(extra_data)] * 5)


class TestCleanCommit(TestCase):

    def test_empty_commit_returns_defualt_value(self):
        empty = '    '.join(['\r\n'] * 10)
        result = github.clean_commit(empty)
        eq_(result, 'Missing commit message.')

    def test_commit_with_whitespace_returns_significant_message(self):
        commit = '    '.join(['\r\n'] * 5)
        commit += 'Hello world!'
        result = github.clean_commit(commit)
        eq_(result, 'Hello world!')

    def test_html_is_stripped(self):
        commit = '    '.join(['\r\n'] * 5)
        commit += '<a href="http://us-ignite.org/">Hello world!</a>'
        result = github.clean_commit(commit)
        eq_(result, 'Hello world!')
