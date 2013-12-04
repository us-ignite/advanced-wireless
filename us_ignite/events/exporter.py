import pytz
# import urllib
from django.utils.http import urlquote


def format_datetime(datetime):
    """Generate an string from ``datetime`` localized to ``UTC``"""
    if not datetime:
        return None
    utc_tz = pytz.timezone('UTC')
    utc_date = utc_tz.normalize(datetime.astimezone(utc_tz))
    # The ``Z`` is hardcoded since ``%z`` returns ``UTC``:
    return utc_date.strftime('%Y%m%dT%H%M%SZ')


def get_google_calendar_url(
        name, start_datetime, end_datetime, description, venue):
    URL = 'https://www.google.com/calendar/render'
    start = format_datetime(start_datetime)
    end = format_datetime(end_datetime)
    # Make start and end are provided:
    if not all([start, end]):
        return None
    data = (
        ('action', 'TEMPLATE'),
        ('text', name),
        ('dates', '%s/%s' % (start, end)),
        ('details', description),
        ('location', venue),
    )
    param_list = ['%s=%s' % (k, urlquote(v)) for k, v in data]
    return u'%s?%s' % (URL, '&'.join(param_list))
