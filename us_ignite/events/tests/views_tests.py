from nose.tools import assert_raises, eq_, ok_
from mock import patch, Mock

from django.contrib.auth.models import User
from django.http import Http404
from django.test import TestCase


from us_ignite.common.tests import utils
from us_ignite.events import views
from us_ignite.events.forms import EventURLFormSet
from us_ignite.events.models import Event
from us_ignite.events.tests import fixtures
from us_ignite.profiles.tests.fixtures import get_user


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
        mock_instance.hubs.all.return_value = []
        mock_get.return_value = mock_instance
        request = utils.get_request(
            'get', '/event/abc/', user=utils.get_anon_mock())
        response = views.event_detail(request, 'abc')
        mock_get.assert_called_once_with(Event, slug__exact='abc')
        mock_instance.is_visible_by.assert_called_once_with(request.user)
        eq_(response.status_code, 200)
        eq_(sorted(response.context_data.keys()),
            ['hub_list', 'is_owner', 'object'])
        eq_(response.template_name, 'events/object_detail.html')


class TestEventDetailICSView(TestCase):

    def _tear_down(self):
        for model in [Event, User]:
            model.objects.all().delete()

    @patch('us_ignite.events.views.get_object_or_404')
    def test_missing_event_raises_404(self, mock_get):
        mock_get.side_effect = Http404
        request = utils.get_request(
            'get', '/event/abc/ics/', user=utils.get_anon_mock())
        assert_raises(Http404, views.event_detail_ics, request, 'abc')
        mock_get.assert_called_once_with(Event.published, slug__exact='abc')

    def test_valid_event_returns_calendar(self):
        user = get_user('ignite-user')
        event = fixtures.get_event(
            user=user, slug='abc', status=Event.PUBLISHED)
        request = utils.get_request(
            'get', '/event/abc/ics/', user=utils.get_anon_mock())
        response = views.event_detail_ics(request, 'abc')
        eq_(response.status_code, 200)
        eq_(response['Content-Disposition'], 'attachment; filename="event.ics"')
        eq_(response['Content-Type'], 'text/calendar')
        ok_(response.content)


class TestEventAddView(TestCase):

    def _tear_down(self):
        for model in [Event, User]:
            model.objects.all().delete()

    def test_add_event_requires_auth(self):
        request = utils.get_request(
            'get', '/event/add/', user=utils.get_anon_mock())
        response = views.event_add(request)
        eq_(response.status_code, 302)
        eq_(response['Location'], utils.get_login_url('/event/add/'))

    def test_event_add_detail(self):
        request = utils.get_request(
            'get', '/event/add/', user=utils.get_user_mock())
        response = views.event_add(request)
        eq_(response.status_code, 200)
        eq_(response.template_name, 'events/object_add.html')
        eq_(sorted(response.context_data.keys()), ['form', 'formset', ])

    def invalid_payload_fails(self):
        user = get_user('ignite-user')
        request = utils.get_request(
            'post', '/event/add/', data={}, user=user)
        response = views.event_add(request)
        eq_(response.status_code, 200)
        ok_(response.context_data['form'].errors)
        self._tear_down()

    def test_valid_payload_succeeds(self):
        user = get_user('ignite-user')
        data = {
            'name': 'Gigabit community',
            'status': Event.DRAFT,
            'start_datetime': '2013-12-14 14:30:59',
            'venue': 'London UK',
            'scope': 1,
            'description': 'Gigabit event',
        }
        formset_data = utils.get_inline_payload(EventURLFormSet)
        data.update(formset_data)
        request = utils.get_request(
            'post', '/event/add/', data=data, user=user)
        request._messages = utils.TestMessagesBackend(request)
        response = views.event_add(request)
        eq_(response.status_code, 302)
        event = Event.objects.get(name='Gigabit community')
        eq_(response['Location'], event.get_absolute_url())
        self._tear_down()


class TestEventListView(TestCase):

    @patch('us_ignite.events.models.Event.published.filter')
    def test_event_list_request_is_successful(self, mock_filter):
        mock_filter.return_value = []
        request = utils.get_request(
            'get', '/events/', user=utils.get_anon_mock())
        response = views.event_list(request)
        eq_(response.status_code, 200)
        eq_(response.template_name, 'events/object_list.html')
        eq_(sorted(response.context_data.keys()), ['page'])
        mock_filter.assert_called_once()


class TestEventEditView(TestCase):

    def _tear_down(self):
        for model in [Event, User]:
            model.objects.all().delete()

    def test_add_event_requires_auth(self):
        request = utils.get_request(
            'get', '/event/foo/edit/', user=utils.get_anon_mock())
        response = views.event_edit(request, 'foo')
        eq_(response.status_code, 302)
        eq_(response['Location'], utils.get_login_url('/event/foo/edit/'))

    def test_event_edit_requires_owner(self):
        user = get_user('ignite-user')
        event = fixtures.get_event(
            user=user, slug='foo', status=Event.PUBLISHED)
        request = utils.get_request(
            'get', event.get_absolute_url(), user=get_user('other'))
        assert_raises(Http404, views.event_edit, request, 'foo')
        self._tear_down()

    def test_event_detail_is_successful(self):
        user = get_user('ignite-user')
        event = fixtures.get_event(
            user=user, slug='foo', status=Event.PUBLISHED)
        request = utils.get_request('get', event.get_absolute_url(), user=user)
        response = views.event_edit(request, 'foo')
        eq_(response.status_code, 200)
        eq_(response.template_name, 'events/object_edit.html')
        eq_(sorted(response.context_data.keys()),
            ['form', 'formset', 'object'])

    def test_event_invalid_payload_fails(self):
        user = get_user('ignite-user')
        event = fixtures.get_event(
            user=user, slug='foo', status=Event.PUBLISHED)
        request = utils.get_request(
            'post', event.get_absolute_url(), data={}, user=user)
        response = views.event_edit(request, 'foo')
        eq_(response.status_code, 200)
        eq_(response.template_name, 'events/object_edit.html')
        ok_(response.context_data['form'].errors)

    def test_valid_payload_is_saved(self):
        user = get_user('ignite-user')
        event = fixtures.get_event(
            user=user, slug='foo', status=Event.PUBLISHED)
        data = {
            'name': 'Gigabit community',
            'status': Event.DRAFT,
            'start_datetime': '2013-12-14 14:30:59',
            'venue': 'London UK',
            'scope': 1,
            'description': 'Gigabit event',
        }
        formset_data = utils.get_inline_payload(EventURLFormSet)
        data.update(formset_data)
        request = utils.get_request(
            'post', event.get_absolute_url(), data=data, user=user)
        request._messages = utils.TestMessagesBackend(request)
        response = views.event_edit(request, 'foo')
        eq_(response.status_code, 302)
        eq_(response['Location'], event.get_absolute_url())
