from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe

from us_ignite.common import output

register = template.Library()


@register.filter(is_safe=True)
@stringfilter
def markdown(value):
    return mark_safe(output.to_html(value))
