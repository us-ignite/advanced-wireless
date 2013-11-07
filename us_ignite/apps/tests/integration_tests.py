from nose.tools import eq_

from django.test import TestCase


class TestAppList(TestCase):

    def test_everyone_can_see_applications(self):
        response = self.client.get('/apps/')
        eq_(response.status_code, 200)
        eq_(len(response.context['page'].object_list), 0)
