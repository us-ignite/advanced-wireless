from django import template
from django.template.loader import render_to_string

from us_ignite.news.models import Article


register = template.Library()


class ArticleNode(template.Node):

    def __init__(self, template_name):
        self.template_name = template_name

    def render(self, context):
        template_name = self.template_name.resolve(context)
        context = {
            'object_list': Article.published.all()[:5]
        }
        return render_to_string(template_name, context)


def render_latest_articles(parser, token):
    """Tag to render the latest ``Articles``.

    Usage:

    {% latest_articles "news/object_short_list.html" %}

    Where the second argument is a template path.
    """
    bits = token.split_contents()
    if not len(bits) == 2:
        raise template.TemplateSyntaxError(
            "%r tag only accepts a template argument." % bits[0])
    # Determine the template name (could be a variable or a string):
    template_name = parser.compile_filter(bits[1])
    return ArticleNode(template_name)


register.tag('latest_articles', render_latest_articles)
