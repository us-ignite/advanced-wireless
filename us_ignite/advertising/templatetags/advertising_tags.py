from django import template
from django.template.loader import render_to_string

from us_ignite.advertising.models import Advert


register = template.Library()


class AdvertisingNode(template.Node):

    def __init__(self, template_name):
        self.template_name = template_name

    def render(self, context):
        template_name = self.template_name.resolve(context)
        advert = Advert.published.get_featured()
        context = {'object': advert}
        return render_to_string(template_name, context)


def render_advertising_box(parser, token):
    """Tag to render the current ``Advertised`` box.

    Usage:

    {% advertising_box "advertising/object_block.html" %}

    Where the second argument is a template path.
    """
    bits = token.split_contents()
    if not len(bits) == 2:
        raise template.TemplateSyntaxError(
            "%r tag only accepts a template argument." % bits[0])
    # Determine the template name (could be a variable or a string):
    template_name = parser.compile_filter(bits[1])
    return AdvertisingNode(template_name)


register.tag('advertising_box', render_advertising_box)
