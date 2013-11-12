from django import template

from us_ignite.apps import aggregator


def render_as_widget(url):
    result = aggregator.render_url(url)
    return result if result else u''


register = template.Library()
register.filter('render_as_widget', render_as_widget)
