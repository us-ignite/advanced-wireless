from nose.tools import eq_

from django.test import TestCase

from us_ignite.events import forms


class TestEventForm(TestCase):

    def test_fields_listed_are_not_sensitive(self):
        form = forms.EventForm()
        eq_(sorted(form.fields.keys()),
            sorted(['name', 'status', 'website', 'image', 'start_datetime',
                    'end_datetime', 'venue', 'description', 'tags', 'hubs'])
        )

    def test_empty_payload_fails(self):
        form = forms.EventForm({})
        eq_(form.is_valid(), False)

    def test_valid_payload_is_successful(self):
        data = {
            'name': 'Gigabit community',
            'status': 1,
            'start_datetime': '2013-12-14 14:30:59',
            'venue': 'London UK',
        }
        form = forms.EventForm(data)
        eq_(form.is_valid(), True)
