from nose.tools import eq_

from django.test import TestCase

from us_ignite.events import forms


class TestEventForm(TestCase):

    def test_fields_listed_are_not_sensitive(self):
        form = forms.EventForm()
        eq_(sorted(form.fields.keys()),
            sorted(['address', 'audience_other', 'audiences',
                    'description', 'end_datetime', 'event_type',
                    'hubs', 'image', 'name', 'position', 'scope',
                    'start_datetime', 'status', 'tags', 'tickets_url',
                    'timezone', 'website', 'actionclusters'])
        )

    def test_empty_payload_fails(self):
        form = forms.EventForm({})
        eq_(form.is_valid(), False)

    def test_valid_payload_is_successful(self):
        data = {
            'name': 'Gigabit community',
            'status': 1,
            'description': 'Gigabit meetup',
            'start_datetime': '2013-12-14 14:30:59',
            'scope': 1,
            'address': 'London UK',
            'timezone': 'US/Eastern',
        }
        form = forms.EventForm(data)
        eq_(form.is_valid(), True)
