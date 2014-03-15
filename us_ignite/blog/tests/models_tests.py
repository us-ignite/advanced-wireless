from datetime import datetime
from nose.tools import eq_, ok_

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from us_ignite.common.tests import utils
from us_ignite.profiles.tests.fixtures import get_user
from us_ignite.blog.models import BlogLink, Post, PostAttachment
from us_ignite.blog.tests import fixtures


class TestPostModel(TestCase):

    def tearDown(self):
        for model in [Post, User]:
            model.objects.all().delete()

    def test_post_is_created_successfully(self):
        author = get_user('us-ignite')
        data = {
            'author': author,
            'slug': 'gigabit-post',
            'title': 'Gigabit post',
        }
        instance = Post.objects.create(**data)
        ok_(instance.id)
        eq_(instance.status, Post.DRAFT)
        eq_(instance.wp_id, '')
        eq_(instance.wp_type, '')
        eq_(instance.title, 'Gigabit post')
        eq_(instance.slug, 'gigabit-post')
        eq_(instance.content, '')
        eq_(instance.content_html, '')
        eq_(instance.excerpt, '')
        eq_(instance.excerpt_html, '')
        eq_(instance.author, author)
        ok_(instance.publication_date)
        ok_(instance.update_date)
        eq_(instance.is_featured, False)
        eq_(list(instance.tags.all()), [])
        ok_(instance.created)
        ok_(instance.modified)
        eq_(instance.attachment, None)
        eq_(instance.image, None)
        eq_(instance.name, 'Gigabit post')

    def test_post_is_published(self):
        author = get_user('us-ignite')
        post = fixtures.get_post(author=author, status=Post.PUBLISHED)
        eq_(post.is_published(), True)

    def test_user_is_author(self):
        author = get_user('us-ignite')
        post = fixtures.get_post(author=author)
        eq_(post.is_author(author), True)

    def test_is_visible_by_anon_user(self):
        author = get_user('us-ignite')
        post = fixtures.get_post(author=author, status=Post.PUBLISHED)
        eq_(post.is_visible_by(utils.get_anon_mock()), True)

    def test_is_not_visible_by_anon(self):
        author = get_user('us-ignite')
        post = fixtures.get_post(author=author, status=Post.DRAFT)
        eq_(post.is_visible_by(utils.get_anon_mock()), False)

    def test_is_visible_by_author(self):
        author = get_user('us-ignite')
        post = fixtures.get_post(author=author, status=Post.DRAFT)
        eq_(post.is_visible_by(author), True)

    def test_get_absolute_url_single_digit_month(self):
        author = get_user('us-ignite')
        naive = datetime(2012, 3, 3, 1, 30)
        publication_date = naive.replace(tzinfo=timezone.utc)
        post = fixtures.get_post(
            author=author, publication_date=publication_date, slug='gigabit-a')
        eq_(post.get_absolute_url(), '/blog/2012/3/gigabit-a/')

    def test_get_absolute_url_double_digit_month(self):
        author = get_user('us-ignite')
        naive = datetime(2012, 10, 3, 1, 30)
        publication_date = naive.replace(tzinfo=timezone.utc)
        post = fixtures.get_post(
            author=author, publication_date=publication_date, slug='gigabit-a')
        eq_(post.get_absolute_url(), '/blog/2012/10/gigabit-a/')


class TestPostAttachmentModel(TestCase):

    def setUp(self):
        for model in [PostAttachment, Post, User]:
            model.objects.all().delete()

    def test_post_attachment_is_created_successfully(self):
        author = get_user('us-ignite')
        post = fixtures.get_post(author=author, status=Post.PUBLISHED)
        data = {
            'post': post,
            'title': 'Gigabit post',
        }
        instance = PostAttachment.objects.create(**data)
        ok_(instance.id)
        eq_(instance.post, post)
        eq_(instance.title, 'Gigabit post')
        eq_(instance.wp_id, '')
        eq_(instance.slug, '')
        eq_(instance.url, '')
        eq_(instance.attachment, '')
        eq_(instance.mime_type, '')
        eq_(instance.description, '')
        eq_(instance.caption, '')


class TestBlogLinkModel(TestCase):

    def test_blog_link_is_created_successfully(self):
        data = {
            'name': 'US Ignite campaign',
            'url': 'http://us-ignite.org',
        }
        link = BlogLink.objects.create(**data)
        ok_(link.pk)
        eq_(link.name, 'US Ignite campaign')
        eq_(link.url, 'http://us-ignite.org')
        ok_(link.created)
        eq_(link.order, 0)
