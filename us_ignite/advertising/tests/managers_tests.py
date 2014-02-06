from nose.tools import eq_

from django.test import TestCase

from us_ignite.advertising.models import Advert
from us_ignite.advertising.tests import fixtures


class TestAdvertPublishedManager(TestCase):

    def tearDown(self):
        Advert.objects.all().delete()

    def test_published_advert_is_returned(self):
        advert = fixtures.get_advert(status=Advert.PUBLISHED)
        eq_(list(Advert.published.all()), [advert])

    def test_unpublished_aerticle_is_not_returned(self):
        fixtures.get_advert(status=Advert.DRAFT)
        eq_(list(Advert.published.all()), [])

    def test_featured_article_is_returned(self):
        advert = fixtures.get_advert(status=Advert.PUBLISHED, is_featured=True)
        eq_(Advert.published.get_featured(), advert)

    def test_non_featured_article_is_not_returned(self):
        fixtures.get_advert(status=Advert.PUBLISHED, is_featured=False)
        eq_(Advert.published.get_featured(), None)
