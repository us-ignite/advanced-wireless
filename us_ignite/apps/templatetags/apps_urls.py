from django import template

from us_ignite.aggregator import renderer


def render_as_widget(url):
    result = renderer.cached_render_url(url)
    return result if result else u''


register = template.Library()
register.filter('render_as_widget', render_as_widget)
