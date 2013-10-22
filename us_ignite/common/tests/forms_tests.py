from django.test import TestCase

from nose.tools import eq_, ok_

from us_ignite.common import forms


ORDER_CHOICES = [
    ('first_name', 'First name'),
    ('-last_name', 'Last name'),
]


class TestOrderForm(TestCase):

    def test_order_form_accepts_order_choices(self):
        form = forms.OrderForm(order_choices=ORDER_CHOICES)
        eq_(form.fields['order'].choices, ORDER_CHOICES)

    def test_form_with_empty_options_has_no_choices(self):
        form = forms.OrderForm()
        eq_(form.fields['order'].choices, [])

    def test_form_is_not_valid_with_invalid_choice(self):
        payload = {'order': 'INVALID'}
        form = forms.OrderForm(payload, order_choices=ORDER_CHOICES)
        eq_(form.is_valid(), False)
        ok_('order' in form.errors)

    def test_form_is_valid_with_valid_choice(self):
        payload = {'order': 'first_name'}
        form = forms.OrderForm(payload, order_choices=ORDER_CHOICES)
        eq_(form.is_valid(), True)

    def test_cleaned_data_is_valid_parameter(self):
        payload = {'order': '-last_name'}
        form = forms.OrderForm(payload, order_choices=ORDER_CHOICES)
        eq_(form.is_valid(), True)
        eq_(form.cleaned_data['order'], '-last_name')
