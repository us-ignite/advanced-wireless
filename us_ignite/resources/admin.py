from django.contrib import admin

from us_ignite.resources.models import Resource, ResourceType, Sector


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'status', 'is_featured')
    search_fields = ('name', 'slug', 'description', 'url')
    list_filter = ('is_featured', 'created')
    date_hierarchy = 'created'
    raw_id_fields = ['contact']


class ResourceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class SectorAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


admin.site.register(Resource, ResourceAdmin)
admin.site.register(ResourceType, ResourceTypeAdmin)
admin.site.register(Sector, SectorAdmin)
