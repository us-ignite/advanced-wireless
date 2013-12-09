from dateutil.relativedelta import relativedelta

from django.utils import timezone

from us_ignite.challenges.models import Challenge, Entry
from us_ignite.profiles.tests.fixtures import get_user


def get_challenge(**kwargs):
    start_date = timezone.now()
    end_date = start_date + relativedelta(days=10)
    data = {
        'name': 'Gigabit challenge',
        'start_datetime': start_date,
        'end_datetime': end_date,
        'summary': 'Summary',
        'description': 'Description',
    }
    if not 'user' in kwargs:
        data['user'] = get_user('us-ignite')
    data.update(kwargs)
    return Challenge.objects.create(**data)


def get_entry(application, **kwargs):
    data = {
        'application': application,
    }
    if not 'challenge' in kwargs:
        data['challenge'] = get_challenge()
    data.update(kwargs)
    return Entry.objects.create(**data)
