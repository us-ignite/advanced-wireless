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

    def test_harmful_link_is_removed(self):
        text = u'<a href="javascript:alert(0);">Link</a>'
        output = sanitizer.sanitize(text)
        eq_(output, '<a>Link</a>')

    def test_script_tags_are_removed(self):
        text = u'<script>alert(0);</script>'
        output = sanitizer.sanitize(text)
        eq_(output, u'alert(0);')
