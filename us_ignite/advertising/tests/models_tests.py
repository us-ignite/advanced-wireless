from nose.tools import eq_, ok_

from django.test import TestCase

from us_ignite.advertising.models import Advert


class TestAdvertModel(TestCase):

    def tearDown(self):
        Advert.objects.all().delete()

    def test_instance_is_created_successfully(self):
        data = {
            'name': 'Gigabit advertising',
            'url': 'http://us-ignite.org/',
            'image': 'ad.png',
        }
        instance = Advert.objects.create(**data)
        ok_(instance.id)
        eq_(instance.name, 'Gigabit advertising')
        eq_(instance.slug, 'gigabit-advertising')
        eq_(instance.status, Advert.DRAFT)
        eq_(instance.url, 'http://us-ignite.org/')
        eq_(instance.image, 'ad.png')
        eq_(instance.is_featured, False)
        ok_(instance.created)
        ok_(instance.modified)
