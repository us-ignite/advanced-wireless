from mock import Mock, patch
from nose.tools import eq_

from django.test import TestCase

from us_ignite.common.tests import utils
from us_ignite.maps import views


patch_related = patch('us_ignite.maps.models.Location.published.select_related')


class TestLocationListView(TestCase):

    @patch_related
    def test_request_is_successful(self, mock_related):
        request = utils.get_request('get', '/maps/')
        response = views.location_list(request)
        mock_related.assert_called_once_with('category')
        mock_related.return_value.all.assert_called_once_with()
        eq_(response.status_code, 200)
        eq_(sorted(response.context_data.keys()), ['object_list', ])
        eq_(response.template_name, 'maps/object_list.html')


class TestGetLocationDataHelper(TestCase):

    def test_data_is_not_sensitive(self):
        mock = Mock()
        response = views._get_location_data(mock)
        eq_(sorted(response.keys()),
            sorted(['latitude', 'longitude', 'name', 'type',
                    'website', 'category', 'image', 'content']))


class TestLocationListJsonView(TestCase):

    @patch_related
    def test_request_is_successful(self, mock_related):
        mock_related.return_value.all.return_value = []
        request = utils.get_request('get', '/maps/location.json')
        response = views.location_list_json(request)
        mock_related.assert_called_once_with('category')
        mock_related.return_value.all.assert_called_once_with()
        eq_(response.status_code, 200)
        eq_(response['Content-Type'], 'application/javascript')
        eq_(response.content, 'map.render([])')
