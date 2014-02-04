from django.contrib import admin

from us_ignite.apps.models import (Application, ApplicationURL,
                                   ApplicationMedia, Domain, Feature,
                                   Page, PageApplication)


class ApplicationURLInline(admin.TabularInline):
    model = ApplicationURL


class ApplicationMediaInline(admin.TabularInline):
    model = ApplicationMedia


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'stage', 'status')
    search_fields = ['name', 'slug', 'summary', 'impact_statement',
                     'description', 'roadmap', 'assistance',
                     'team_description', 'notes', 'acknowledgments']
    list_filter = ['stage', 'domain__name', 'status', 'created', ]
    date_hierarchy = 'created'
    inlines = [ApplicationURLInline, ApplicationMediaInline]


class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class PageApplicationInline(admin.TabularInline):
    raw_id_fields = ('application', )
    model = PageApplication


class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'status', 'created', )
    list_filter = ('status', 'created', )
    date_hierarchy = 'created'
    inlines = [PageApplicationInline]

admin.site.register(Application, ApplicationAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Page, PageAdmin)
