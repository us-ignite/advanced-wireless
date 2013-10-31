from nose.tools import ok_, eq_

from django.test import TestCase

from us_ignite.profiles import exporter


class TestCSVResponse(TestCase):

    def test_valid_response(self):
        row_list = [(1, '2', 3.0)]
        response = exporter.csv_response('export', row_list)
        eq_(response['Content-Disposition'],
            'attachment; filename="export.csv"')
        ok_('1,2,3.0' in response.content)
