from django import template
from django.template.loader import render_to_string

from us_ignite.sections.models import Sponsor


register = template.Library()


class RenderingNode(template.Node):

    def __init__(self, template_name):
        self.template_name = template_name

    def render(self, context):
        template_name = self.template_name.resolve(context)
        context.update({
            'object_list': Sponsor.objects.all()
        })
        return render_to_string(template_name, context)


def _render_sponsors(parser, token):
    """Tag to render the latest ``Articles``.

    Usage:

    {% render_sponsors "sections/sponsor_list.html" %}

    Where the second argument is a template path.
    """
    bits = token.split_contents()
    if not len(bits) == 2:
        raise template.TemplateSyntaxError(
            "%r tag only accepts a template argument." % bits[0])
    # Determine the template name (could be a variable or a string):
    template_name = parser.compile_filter(bits[1])
    return RenderingNode(template_name)

register.tag('render_sponsors', _render_sponsors)
