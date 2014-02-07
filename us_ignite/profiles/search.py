import watson

from us_ignite.common import render


class ProfileSearchAdapter(watson.SearchAdapter):

    def get_title(self, obj):
        return obj.name

    def get_description(self, obj):
        return obj.bio

    def get_content(self, obj):
        fields = [
            ', '.join([t.name for t in obj.tags.all()]),
        ]
        return render.render_fields(fields)
