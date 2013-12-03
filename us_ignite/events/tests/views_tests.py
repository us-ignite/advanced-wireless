from nose.tools import eq_, raises, assert_raises
from mock import patch

from django.test import TestCase
from django.http import Http404

from us_ignite.common.tests import utils
from us_ignite.events import views
from us_ignite.events.models import Event


class TestEventDetailView(TestCase):

    @patch('us_ignite.events.views.get_object_or_404')
    def test_missing_event_raises_404(self, mock_get):
        mock_get.side_effect = Http404
        request = utils.get_request('get', '/event/abc/')
        assert_raises(Http404, views.event_detail, request, 'abc')
        mock_get.assert_called_once_with(Event.published, slug__exact='abc')

    @patch('us_ignite.events.views.get_object_or_404')
    def test_get_request_is_valid(self, mock_get):
        request = utils.get_request('get', '/event/abc/')
        response = views.event_detail(request, 'abc')
        mock_get.assert_called_once_with(Event.published, slug__exact='abc')
        eq_(response.status_code, 200)
        eq_(sorted(response.context_data.keys()), ['object'])
        eq_(response.template_name, 'events/object_detail.html')
