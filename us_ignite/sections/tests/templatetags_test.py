from mock import patch
from nose.tools import ok_, raises

from django.test import TestCase
from django.template import Template, Context, TemplateSyntaxError


class TestRenderSponsorsTemplateTag(TestCase):

    @patch('us_ignite.sections.models.Sponsor.objects.all')
    def test_tag_is_render_successfully(self, all_mock):
        output = Template(
            "{% load sections_tags %}"
            "{% render_sponsors 'sections/sponsor_list.html' %}"
        ).render(Context())
        ok_(output)
        all_mock.assert_called_once_with()

    @raises(TemplateSyntaxError)
    def test_missing_template_raises_error(self):
        Template(
            "{% load sections_tags %}"
            "{% render_sponsors %}"
        ).render(Context())
