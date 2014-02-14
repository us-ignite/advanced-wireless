from mock import patch
from nose.tools import eq_, ok_, raises

from django.test import TestCase
from django.template import Template, Context, TemplateSyntaxError

from us_ignite.snippets.models import Snippet


class TestRenderSnippetTemplateTag(TestCase):

    @patch('us_ignite.snippets.models.Snippet.published.get')
    def test_featured_box_is_rendered_successfully(self, mock_get):
        mock_get.return_value = Snippet(name='Hello!')
        output = Template(
            "{% load snippets_tags %}"
            "{% snippet 'featured' 'snippets/featured.html' %}"
        ).render(Context())
        ok_(output)

    @patch('us_ignite.snippets.models.Snippet.published.get')
    def test_missing_content_is_not_rendered(self, mock_get):
        mock_get.side_effect = Snippet.DoesNotExist
        output = Template(
            "{% load snippets_tags %}"
            "{% snippet 'featured' 'snippets/featured.html' %}"
        ).render(Context())
        eq_(output, u'')

    @raises(TemplateSyntaxError)
    @patch('us_ignite.snippets.models.Snippet.published.get')
    def test_missing_arguments_raises_error(self, mock_get):
        output = Template(
            "{% load snippets_tags %}"
            "{% snippet 'featured's %}"
        ).render(Context())
