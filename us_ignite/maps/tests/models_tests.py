from nose.tools import eq_, ok_

from django.test import TestCase

from us_ignite.maps.models import Category, Location
from us_ignite.maps.tests import fixtures


class TestCategoryModel(TestCase):

    def tearDown(self):
        Category.objects.all().delete()

    def test_instance_is_created_successfully(self):
        data = {
            'name': 'Gigabit Network',
            'slug': 'gigabit-network',
        }
        instance = Category.objects.create(**data)
        ok_(instance.id)
        eq_(instance.name, 'Gigabit Network')
        eq_(instance.slug, 'gigabit-network')


class TestLocationModel(TestCase):

    def tearDown(self):
        for model in [Location, Category]:
            model.objects.all().delete()

    def test_instance_is_created_successfully(self):
        category = fixtures.get_category()
        data = {
            'name': 'Gigabit Hub',
            'category': category,
        }
        instance = Location.objects.create(**data)
        ok_(instance.id)
        eq_(instance.name, 'Gigabit Hub')
        eq_(instance.website, '')
        ok_(instance.position)
        eq_(instance.category, category)
        ok_(instance.created)
        ok_(instance.modified)

    def test_get_image_url_is_from_location(self):
        category = fixtures.get_category()
        instance = fixtures.get_location(category=category, image='foo.png')
        eq_(instance.get_image_url(), '/media/foo.png')

    def test_get_image_url_is_from_category(self):
        category = fixtures.get_category(image='boo.png')
        instance = fixtures.get_location(category=category)
        eq_(instance.get_image_url(), '/media/boo.png')

    def test_get_image_url_is_empty(self):
        category = fixtures.get_category()
        instance = fixtures.get_location(category=category)
        eq_(instance.get_image_url(), '')
