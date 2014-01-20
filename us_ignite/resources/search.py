import watson

from us_ignite.common import render


class ResourceSearchAdapter(watson.SearchAdapter):

    def get_title(self, obj):
        return obj.name

    def get_description(self, obj):
        return obj.description

    def get_content(self, obj):
        fields = [
            self.url,
            self.asset.url if self.asset else '',
            ', '.join([t.name for t in obj.tags.all()]),
        ]
        return render.render_fields(fields)
