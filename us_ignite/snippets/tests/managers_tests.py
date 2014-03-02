from nose.tools import eq_

from django.test import TestCase

from us_ignite.snippets.models import Snippet
from us_ignite.snippets.tests import fixtures


class TestSnippetPublishedManager(TestCase):

    def tearDown(self):
        Snippet.objects.all().delete()

    def test_published_snippet_is_returned(self):
        snippet = fixtures.get_snippet(status=Snippet.PUBLISHED)
        eq_(list(Snippet.published.all()), [snippet])

    def test_unpublished_aerticle_is_not_returned(self):
        fixtures.get_snippet(status=Snippet.DRAFT)
        eq_(list(Snippet.published.all()), [])

    def test_featured_article_is_returned(self):
        snippet = fixtures.get_snippet(status=Snippet.PUBLISHED, is_featured=True)
        eq_(Snippet.published.get_featured(), snippet)

    def test_non_featured_article_is_not_returned(self):
        fixtures.get_snippet(status=Snippet.PUBLISHED, is_featured=False)
        eq_(Snippet.published.get_featured(), None)

    def test_existing_key_is_returned(self):
        snippet = fixtures.get_snippet(
            status=Snippet.PUBLISHED, slug='gigabit')
        eq_(Snippet.published.get_from_key('gigabit'), snippet)

    def test_missing_key_returns_none(self):
        eq_(Snippet.published.get_from_key('gigabit'), None)
