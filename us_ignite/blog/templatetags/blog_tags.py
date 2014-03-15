from django import template
from django.template.loader import render_to_string

from us_ignite.blog.models import BlogLink


register = template.Library()


class BlogLinkNode(template.Node):

    def __init__(self, template_name):
        self.template_name = template_name

    def render(self, context):
        template_name = self.template_name.resolve(context)
        context = {
            'object_list': BlogLink.objects.all()[:10]
        }
        return render_to_string(template_name, context)


def render_latest_blog_links(parser, token):
    """Tag to render the latest ``BlogLinks``.

    Usage:

    {% latest_blog_links "blog/links_short_list.html" %}

    Where the second argument is a template path.
    """
    bits = token.split_contents()
    if not len(bits) == 2:
        raise template.TemplateSyntaxError(
            "%r tag only accepts a template argument." % bits[0])
    # Determine the template name (could be a variable or a string):
    template_name = parser.compile_filter(bits[1])
    return BlogLinkNode(template_name)


register.tag('latest_blog_links', render_latest_blog_links)
