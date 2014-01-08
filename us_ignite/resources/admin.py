from django.contrib import admin

from us_ignite.resources.models import Resource


class ResourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'status', 'is_featured')
    search_fields = ('name', 'slug', 'description', 'url')
    list_filter = ('is_featured', 'created')
    date_hierarchy = 'created'
    raw_id_fields = ['owner', ]

admin.site.register(Resource, ResourceAdmin)
