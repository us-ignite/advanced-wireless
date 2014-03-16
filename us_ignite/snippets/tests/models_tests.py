from nose.tools import eq_, ok_

from django.test import TestCase

from us_ignite.snippets.models import Snippet


class TestSnippetModel(TestCase):

    def tearDown(self):
        Snippet.objects.all().delete()

    def get_instance(self):
        data = {
            'name': 'Gigabit snippets',
            'slug': 'featured',
            'url': 'http://us-ignite.org/',
        }
        return Snippet.objects.create(**data)

    def test_instance_is_created_successfully(self):
        instance = self.get_instance()
        eq_(instance.name, 'Gigabit snippets')
        eq_(instance.status, Snippet.DRAFT)
        eq_(instance.url, 'http://us-ignite.org/')
        eq_(instance.url_text, '')
        eq_(instance.body, '')
        eq_(instance.image, '')
        eq_(instance.is_featured, False)
        ok_(instance.created)
        ok_(instance.modified)
        eq_(instance.slug, 'featured')
        ok_(instance.id)
        eq_(instance.notes, '')
