from django.contrib import admin

from us_ignite.actionclusters.models import (
    ActionCluster,
    ActionClusterURL,
    ActionClusterMedia,
    Domain,
    Feature,
    Year
)


class ActionClusterURLInline(admin.TabularInline):
    model = ActionClusterURL


class ActionClusterMediaInline(admin.TabularInline):
    model = ActionClusterMedia


class ActionClusterAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'stage', 'status', 'is_approved')
    search_fields = ['name', 'slug', 'summary', 'impact_statement',
                     'assistance', 'team_description', 'notes',
                     'acknowledgments']
    list_filter = ['stage', 'domain__name', 'status', 'created', 'is_approved', 'year']
    date_hierarchy = 'created'
    inlines = [ActionClusterURLInline, ActionClusterMediaInline]


class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

class YearAdmin(admin.ModelAdmin):
    list_display = ('year', 'default_year')

admin.site.register(ActionCluster, ActionClusterAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Year, YearAdmin)