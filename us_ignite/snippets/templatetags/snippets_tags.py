from django import template
from django.template.loader import render_to_string

from us_ignite.snippets.models import Snippet


register = template.Library()


class SnippetsNode(template.Node):

    def __init__(self, key, template_name):
        self.key = key
        self.template_name = template_name

    def render(self, context):
        key = self.key.resolve(context)
        template_name = self.template_name.resolve(context)
        try:
            snippet = Snippet.published.get(slug=key)
        except Snippet.DoesNotExist:
            return u''
        template_context = {'object': snippet}
        return render_to_string(template_name, template_context)


def render_snippets_box(parser, token):
    """Tag to render the selected ``Snippet`` box.

    Usage:

    {% snippet KEY TEMPLATE_PATH %}

    Where:
    - ``KEY`` is the slug of the ``Snippet``
    - ``TEMPLATE_PATH`` is the path to the template to be rendered.
    """
    bits = token.split_contents()
    if not len(bits) == 3:
        raise template.TemplateSyntaxError(
            "%r tag requires exactly two arguments." % bits[0])
    key = parser.compile_filter(bits[1])
    template_name = parser.compile_filter(bits[2])
    return SnippetsNode(key, template_name)


register.tag('snippet', render_snippets_box)
