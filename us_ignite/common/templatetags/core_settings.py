from django import template
from django.conf import settings

register = template.Library()


@register.simple_tag
def get_setting(name):
    """Returns a given value from the settings if existing."""
    return getattr(settings, name, "")
