from nose.tools import eq_

from django.test import TestCase

from us_ignite.common import render


class TestRenderFields(TestCase):

    def test_fields_are_rendered_correctly(self):
        fields = [
            'foo',
            '',
        ]
        result = render.render_fields(fields)
        eq_(result, 'foo')
