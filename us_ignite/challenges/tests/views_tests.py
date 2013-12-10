from mock import patch
from nose.tools import eq_

from django.test import TestCase

from us_ignite.common.tests import utils
from us_ignite.challenges import views
from us_ignite.challenges.models import Challenge


patch_filter = patch('us_ignite.challenges.models.Challenge.objects.filter')
patch_now = patch('django.utils.timezone.now')


class TestChallengeListView(TestCase):

    @patch_filter
    @patch_now
    def test_challenge_request_is_successful(self, mock_now, mock_filter):
        mock_now.return_value = 'now'
        request = utils.get_request('get', '/challenges/')
        response = views.challenge_list(request)
        eq_(response.status_code, 200)
        eq_(response.template_name, 'challenges/object_list.html')
        eq_(sorted(response.context_data.keys()), ['object_list'])
        mock_now.assert_called_once_with()
        mock_filter.assert_called_once_with(
            end_datetime__gte='now', status=Challenge.PUBLISHED)
