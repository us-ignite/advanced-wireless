from django.contrib import admin

from us_ignite.events.models import Event


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'start_datetime', 'is_featured')
    search_fields = ('name', 'slug', 'venue', 'description', 'notes')
    list_filter = ('status', 'start_datetime', 'is_featured', 'created')
    date_hierarchy = 'start_datetime'

admin.site.register(Event, EventAdmin)
