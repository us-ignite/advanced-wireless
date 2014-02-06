from nose.tools import eq_

from django.test import TestCase

from us_ignite.news.models import Article
from us_ignite.news.tests import fixtures


class TestArticlePublishedManager(TestCase):

    def tearDown(self):
        Article.objects.all().delete()

    def test_published_article_is_returned(self):
        article = fixtures.get_article(status=Article.PUBLISHED)
        eq_(list(Article.published.all()), [article])

    def test_unpublished_aerticle_is_not_returned(self):
        fixtures.get_article(status=Article.DRAFT)
        eq_(list(Article.published.all()), [])
