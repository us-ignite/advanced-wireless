from django.contrib import admin

from us_ignite.apps.models import Application, ApplicationURL


class ApplicationURLInline(admin.TabularInline):
    model = ApplicationURL


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'stage', 'status')
    search_fields = ['name', 'slug', 'short_description', 'description']
    list_filter = ['stage', 'status', 'created']
    date_hierarchy = 'created'
    inlines = [ApplicationURLInline]

admin.site.register(Application, ApplicationAdmin)
