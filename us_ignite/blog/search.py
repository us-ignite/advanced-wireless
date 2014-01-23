import watson

from us_ignite.common import render
from django.utils.html import strip_tags


class PostSearchAdapter(watson.SearchAdapter):

    def get_title(self, obj):
        return obj.title

    def get_description(self, obj):
        return strip_tags(obj.excerpt_html)

    def get_content(self, obj):
        fields = [
            strip_tags(obj.content_html),
            ', '.join([t.name for t in obj.tags.all()]),
        ]
        return render.render_fields(fields)
