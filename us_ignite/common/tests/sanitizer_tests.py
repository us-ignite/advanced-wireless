from nose.tools import eq_

from django.test import TestCase

from us_ignite.common import sanitizer


class TestSanitizeFunction(TestCase):

    def test_valid_text_is_not_modified(self):
        text = u'<p>Hello!</p>'
        output = sanitizer.sanitize(text)
        eq_(output, '<p>Hello!</p>')

    def test_invalid_tag_is_removed(self):
        text = u'<p><font size="20">Hello!</font></p>'
        output = sanitizer.sanitize(text)
        eq_(output, '<p>Hello!</p>')
