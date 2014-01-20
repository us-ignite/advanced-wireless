from nose.tools import eq_, ok_

from django.test import TestCase

from us_ignite.search import forms


class TestTagSearchForm(TestCase):

    def test_fields_are_not_sensitive(self):
        form = forms.TagSearchForm()
        eq_(sorted(form.fields.keys()), ['tag'])

    def test_empty_payload_is_invalid(self):
        form = forms.TagSearchForm({})
        eq_(form.is_valid(), False)

    def test_valid_payload(self):
        form = forms.TagSearchForm({'tag': 'gigabit'})
        eq_(form.is_valid(), True)

    def test_long_payload_fails(self):
        tag_name = 'a' * 51
        form = forms.TagSearchForm({'tag': tag_name})
        eq_(form.is_valid(), False)
        ok_(form.errors['tag'])


class TestSearchForm(TestCase):

    def test_fields_are_not_sensitive(self):
        form = forms.SearchForm()
        eq_(sorted(form.fields.keys()), ['q'])

    def test_empty_payload_is_invalid(self):
        form = forms.SearchForm({})
        eq_(form.is_valid(), False)

    def test_valid_payload(self):
        form = forms.SearchForm({'q': 'gigabit'})
        eq_(form.is_valid(), True)

    def test_long_payload_fails(self):
        q_name = 'a' * 51
        form = forms.SearchForm({'q': q_name})
        eq_(form.is_valid(), False)
        ok_(form.errors['q'])
