from nose.tools import eq_, assert_raises
from mock import patch, Mock

from django.test import TestCase
from django.http import Http404

from us_ignite.common.tests import utils
from us_ignite.events import views
from us_ignite.events.models import Event


class TestEventDetailView(TestCase):

    @patch('us_ignite.events.views.get_object_or_404')
    def test_missing_event_raises_404(self, mock_get):
        mock_get.side_effect = Http404
        request = utils.get_request(
            'get', '/event/abc/', user=utils.get_anon_mock())
        assert_raises(Http404, views.event_detail, request, 'abc')
        mock_get.assert_called_once_with(Event, slug__exact='abc')

    @patch('us_ignite.events.views.get_object_or_404')
    def test_not_visible_event_raises_404(self, mock_get):
        mock_instance = Mock(spec=Event)()
        mock_instance.is_visible_by.return_value = False
        mock_get.return_value = mock_instance
        request = utils.get_request(
            'get', '/event/abc/', user=utils.get_anon_mock())
        assert_raises(Http404, views.event_detail, request, 'abc')
        mock_get.assert_called_once_with(Event, slug__exact='abc')
        mock_instance.is_visible_by.assert_called_once()

    @patch('us_ignite.events.views.get_object_or_404')
    def test_get_request_is_valid(self, mock_get):
        mock_instance = Mock(spec=Event)()
        mock_instance.is_visible_by.return_value = True
        mock_get.return_value = mock_instance
        request = utils.get_request(
            'get', '/event/abc/', user=utils.get_anon_mock())
        response = views.event_detail(request, 'abc')
        mock_get.assert_called_once_with(Event, slug__exact='abc')
        eq_(response.status_code, 200)
        eq_(sorted(response.context_data.keys()), ['object'])
        eq_(response.template_name, 'events/object_detail.html')
        mock_instance.is_visible_by.assert_called_once_with(request.user)
        mock_instance.is_visible_by.assert_called_once()
