from django.contrib import admin

from us_ignite.hubs.models import Hub, HubActivity


class HubAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'status', 'created')
    search_fields = ('name', 'slug', 'description', 'features')
    date_hierarchy = 'created'
    list_filter = ('status', 'created')


class HubActivityAdmin(admin.ModelAdmin):
    list_display = ('name', 'created')
    search_fields = ('name', 'description')
    date_hierarchy = 'created'
    list_filter = ('created', )

admin.site.register(Hub, HubAdmin)
admin.site.register(HubActivity, HubActivityAdmin)
