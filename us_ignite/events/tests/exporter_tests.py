import datetime
import pytz
import urlparse

from nose.tools import eq_

from django.test import TestCase

from us_ignite.events import exporter


class TestFormatDateTime(TestCase):

    def test_missing_format_datetime_returns_undefined(self):
        result = exporter.format_datetime(None)
        eq_(result, None)

    def test_timezone_is_formatted(self):
        ny_tz = pytz.timezone("America/New_York")
        ny = ny_tz.localize(datetime.datetime(2013, 12, 2, 12, 00, 00))
        result = exporter.format_datetime(ny)
        # New York is -5GMT/UTC:
        eq_(result, '20131202T170000Z')


class TestGetGoogleCalendarURL(TestCase):

    def test_all_day_event_is_successful(self):
        ny_tz = pytz.timezone("America/New_York")
        start = ny_tz.localize(datetime.datetime(2013, 12, 2, 12, 00))
        end = ny_tz.localize(datetime.datetime(2013, 12, 2, 13, 00))
        result = exporter.get_google_calendar_url(
            'Gigabit event', start, end,  'Community meet-up', 'Somewhere')
        parsed_url = urlparse.urlparse(result)
        eq_(parsed_url.netloc, 'www.google.com')
        eq_(parsed_url.path, '/calendar/render')
        parsed_qs = urlparse.parse_qs(parsed_url.query)
        eq_(parsed_qs, {
            u'action': [u'TEMPLATE'],
            u'text': [u'Gigabit event'],
            u'dates': [u'20131202T170000Z/20131202T180000Z'],
            u'details': [u'Community meet-up'],
            u'location': [u'Somewhere']
        })
