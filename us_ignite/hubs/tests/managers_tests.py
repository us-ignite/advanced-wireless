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

    def test_featured_hub_is_returned(self):
        hub = fixtures.get_hub(status=Hub.PUBLISHED, is_featured=True)
        eq_(Hub.active.get_featured(), hub)

    def test_not_featured_hub_returns_none(self):
        hub = fixtures.get_hub(status=Hub.PUBLISHED, is_featured=False)
        eq_(Hub.active.get_featured(), None)
