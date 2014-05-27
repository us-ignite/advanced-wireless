import watson

from us_ignite.common import render


class HubSearchAdapter(watson.SearchAdapter):

    def get_title(self, obj):
        return obj.name

    def get_description(self, obj):
        return obj.summary

    def get_content(self, obj):
        fields = [
            obj.description,
            ', '.join([f.name for f in obj.features.all()]),
            ', '.join([t.name for t in obj.tags.all()]),
        ]
        return render.render_fields(fields)
