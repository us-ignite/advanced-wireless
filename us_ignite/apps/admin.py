from django.contrib import admin

from us_ignite.apps.models import (Application, ApplicationURL,
                                   ApplicationImage, Domain, Feature,
                                   Page, PageApplication)


class ApplicationURLInline(admin.TabularInline):
    model = ApplicationURL


class ApplicationImageInline(admin.TabularInline):
    model = ApplicationImage


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'stage', 'status')
    search_fields = ['name', 'slug', 'short_description', 'description']
    list_filter = ['stage', 'status', 'created']
    date_hierarchy = 'created'
    inlines = [ApplicationURLInline, ApplicationImageInline]


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
