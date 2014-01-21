from dateutil.relativedelta import relativedelta
from nose.tools import eq_

from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone

from us_ignite.blog.models import Entry
from us_ignite.blog.tests import fixtures
from us_ignite.profiles.tests.fixtures import get_user


class TestEntryPublishedManager(TestCase):

    def tearDown(self):
        for model in [Entry, User]:
            model.objects.all().delete()

    def test_published_entry_is_returned(self):
        author = get_user('us-ignite')
        publication_date = timezone.now() - relativedelta(days=1)
        entry = fixtures.get_entry(
            author=author, status=Entry.PUBLISHED,
            publication_date=publication_date)
        eq_(list(Entry.published.all()), [entry])

    def test_published_entry_in_the_future_is_not_returned(self):
        author = get_user('us-ignite')
        publication_date = timezone.now() + relativedelta(days=1)
        entry = fixtures.get_entry(
            author=author, status=Entry.PUBLISHED,
            publication_date=publication_date)
        eq_(list(Entry.published.all()), [])

    def test_draft_entry_is_not_returned(self):
        author = get_user('us-ignite')
        publication_date = timezone.now() - relativedelta(days=1)
        entry = fixtures.get_entry(
            author=author, status=Entry.DRAFT,
            publication_date=publication_date)
        eq_(list(Entry.published.all()), [])

    def test_removed_entry_is_not_returned(self):
        author = get_user('us-ignite')
        publication_date = timezone.now() - relativedelta(days=1)
        entry = fixtures.get_entry(
            author=author, status=Entry.REMOVED,
            publication_date=publication_date)
        eq_(list(Entry.published.all()), [])
