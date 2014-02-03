from nose.tools import eq_

from django.test import TestCase

from us_ignite.maps.models import Category, Location
from us_ignite.maps.tests import fixtures


class TestPublishedLocationManager(TestCase):

    def tearDown(self):
        for model in [Location, Category]:
            model.objects.all().delete()

    def test_published_locations_are_shown(self):
        category = fixtures.get_category()
        location = fixtures.get_location(
            category=category, status=Location.PUBLISHED)
        eq_(list(Location.published.all()), [location])

    def test_unpublished_locations_are_not_shown(self):
        category = fixtures.get_category()
        fixtures.get_location(category=category, status=Location.DRAFT)
        eq_(list(Location.published.all()), [])
