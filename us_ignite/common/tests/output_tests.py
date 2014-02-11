from nose.tools import eq_

from django.test import TestCase

from us_ignite.common import output


class TestHTMLFilter(TestCase):

    def test_filter_produces_html(self):
        html = output.to_html('Hello World!')
        eq_(html, u'<p>Hello World!</p>')

    def test_filter_escapes_html(self):
        html = output.to_html('<script>alert(0);</script>')
        eq_(html, u'<p>&lt;script&gt;alert(0);&lt;/script&gt;</p>')


class TestPrepareTagFunction(TestCase):

    def test_tags_are_changed_to_lowercase(self):
        tag_list = ['Hello', 'World']
        result = output.prepare_tags(tag_list)
        eq_(result, ['hello', 'world'])
