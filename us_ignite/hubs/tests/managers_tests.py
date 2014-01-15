from nose.tools import eq_

from django.test import TestCase

from us_ignite.hubs.models import Hub
from us_ignite.hubs.tests import fixtures


class TestHubActiveManager(TestCase):

    def tearDown(self):
        Hub.objects.all().delete()

    def test_published_hubs_are_listed(self):
        hub = fixtures.get_hub(name='gigabit', status=Hub.PUBLISHED)
        eq_(list(Hub.active.all()), [hub])

    def test_unpublished_hubs_are_not_listed(self):
        hub = fixtures.get_hub(name='gigabit', status=Hub.DRAFT)
        eq_(list(Hub.active.all()), [])
