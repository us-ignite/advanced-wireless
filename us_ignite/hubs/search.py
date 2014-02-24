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
            obj.connections,
            obj.estimated_passes,
            ', '.join([f.name for f in obj.features.all()]),
            ', '.join([t.name for t in obj.tags.all()]),
        ]
        if obj.network_speed:
            fields.append(obj.network_speed.name)
        if obj.organization:
            fields.append(obj.organization.name)
        return render.render_fields(fields)
