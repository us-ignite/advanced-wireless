from dateutil.relativedelta import relativedelta
from nose.tools import eq_

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from us_ignite.blog.models import Post
from us_ignite.blog.tests import fixtures
from us_ignite.profiles.tests.fixtures import get_user


class TestPostPublishedManager(TestCase):

    def tearDown(self):
        for model in [Post, User]:
            model.objects.all().delete()

    def test_published_post_is_returned(self):
        author = get_user('us-ignite')
        publication_date = timezone.now() - relativedelta(days=1)
        post = fixtures.get_post(
            author=author, status=Post.PUBLISHED,
            publication_date=publication_date)
        eq_(list(Post.published.all()), [post])

    def test_published_post_in_the_future_is_not_returned(self):
        author = get_user('us-ignite')
        publication_date = timezone.now() + relativedelta(days=1)
        post = fixtures.get_post(
            author=author, status=Post.PUBLISHED,
            publication_date=publication_date)
        eq_(list(Post.published.all()), [])

    def test_draft_post_is_not_returned(self):
        author = get_user('us-ignite')
        publication_date = timezone.now() - relativedelta(days=1)
        post = fixtures.get_post(
            author=author, status=Post.DRAFT,
            publication_date=publication_date)
        eq_(list(Post.published.all()), [])

    def test_removed_post_is_not_returned(self):
        author = get_user('us-ignite')
        publication_date = timezone.now() - relativedelta(days=1)
        post = fixtures.get_post(
            author=author, status=Post.REMOVED,
            publication_date=publication_date)
        eq_(list(Post.published.all()), [])
