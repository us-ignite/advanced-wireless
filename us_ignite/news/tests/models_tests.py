from nose.tools import eq_, ok_

from django.test import TestCase

from us_ignite.news.models import Article


class TestArticleModel(TestCase):

    def tearDown(self):
        Article.objects.all().delete()

    def test_instance_is_created_successfully(self):
        data = {
            'name': 'Gigabit news',
            'url': 'http://us-ignite.org/',
        }
        instance = Article.objects.create(**data)
        ok_(instance.id)
        eq_(instance.name, 'Gigabit news')
        eq_(instance.status, Article.DRAFT)
        eq_(instance.url, 'http://us-ignite.org/')
        eq_(instance.is_featured, False)
        ok_(instance.created)
        ok_(instance.modified)

    def test_get_get_absolute_url_is_url(self):
        data = {
            'name': 'Gigabit news',
            'url': 'http://us-ignite.org/',
        }
        instance = Article.objects.create(**data)
        eq_(instance.get_absolute_url(), 'http://us-ignite.org/')
