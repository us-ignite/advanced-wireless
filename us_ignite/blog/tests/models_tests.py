from datetime import datetime
from nose.tools import eq_, ok_

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from us_ignite.common.tests import utils
from us_ignite.profiles.tests.fixtures import get_user
from us_ignite.blog.models import Entry
from us_ignite.blog.tests import fixtures


class TestEntryModel(TestCase):

    def tearDown(self):
        for model in [Entry, User]:
            model.objects.all().delete()

    def test_entry_is_created_successfully(self):
        author = get_user('us-ignite')
        data = {
            'author': author,
            'slug': 'gigabit-entry',
            'title': 'Gigabit entry',
            'body': 'Lorem Ipsum',
        }
        instance = Entry.objects.create(**data)
        ok_(instance.id)
        eq_(instance.author, author)
        ok_(instance.publication_date)
        eq_(instance.slug, 'gigabit-entry')
        eq_(instance.status, Entry.DRAFT)
        eq_(instance.title, 'Gigabit entry')
        eq_(instance.body, 'Lorem Ipsum')
        eq_(instance.body_html, 'Lorem Ipsum')
        eq_(instance.summary, '')
        eq_(instance.summary_html, '')
        eq_(instance.image, '')
        eq_(instance.is_featured, False)
        eq_(list(instance.tags.all()), [])
        ok_(instance.created)
        ok_(instance.modified)

    def test_entry_is_published(self):
        author = get_user('us-ignite')
        entry = fixtures.get_entry(author=author, status=Entry.PUBLISHED)
        eq_(entry.is_published(), True)

    def test_user_is_author(self):
        author = get_user('us-ignite')
        entry = fixtures.get_entry(author=author)
        eq_(entry.is_author(author), True)

    def test_is_visible_by_anon_user(self):
        author = get_user('us-ignite')
        entry = fixtures.get_entry(author=author, status=Entry.PUBLISHED)
        eq_(entry.is_visible_by(utils.get_anon_mock()), True)

    def test_is_not_visible_by_anon(self):
        author = get_user('us-ignite')
        entry = fixtures.get_entry(author=author, status=Entry.DRAFT)
        eq_(entry.is_visible_by(utils.get_anon_mock()), False)

    def test_is_visible_by_author(self):
        author = get_user('us-ignite')
        entry = fixtures.get_entry(author=author, status=Entry.DRAFT)
        eq_(entry.is_visible_by(author), True)

    def test_get_absolute_url_single_digit_month(self):
        author = get_user('us-ignite')
        naive = datetime(2012, 3, 3, 1, 30)
        publication_date = naive.replace(tzinfo=timezone.utc)
        entry = fixtures.get_entry(
            author=author, publication_date=publication_date, slug='gigabit-a')
        eq_(entry.get_absolute_url(), '/blog/2012/3/gigabit-a/')

    def test_get_absolute_url_double_digit_month(self):
        author = get_user('us-ignite')
        naive = datetime(2012, 10, 3, 1, 30)
        publication_date = naive.replace(tzinfo=timezone.utc)
        entry = fixtures.get_entry(
            author=author, publication_date=publication_date, slug='gigabit-a')
        eq_(entry.get_absolute_url(), '/blog/2012/10/gigabit-a/')
