from django.contrib import admin

from us_ignite.apps.models import Application, ApplicationURL, ApplicationImage


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

admin.site.register(Application, ApplicationAdmin)
