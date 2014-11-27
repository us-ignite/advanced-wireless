import watson

from us_ignite.common import render


class ActionClusterSearchAdapter(watson.SearchAdapter):

    def get_title(self, obj):
        return obj.name

    def get_description(self, obj):
        return obj.summary

    def get_content(self, obj):
        domain = obj.domain.name if obj.domain else ''
        fields = [
            obj.summary,
            obj.impact_statement,
            obj.assistance,
            obj.team_description,
            obj.acknowledgments,
            ', '.join([t.name for t in obj.tags.all()]),
            domain,
            ', '.join([f.name for f in obj.features.all()]),
        ]
        return render.render_fields(fields)
