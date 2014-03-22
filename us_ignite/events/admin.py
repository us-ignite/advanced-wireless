from django.contrib import admin

from us_ignite.events.models import Audience, Event, EventURL


class AudienceAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', )


class EventURLAdminInline(admin.TabularInline):
    model = EventURL


class EventAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'start_datetime', 'is_featured')
    search_fields = ('name', 'slug', 'address', 'description', 'notes')
    list_filter = ('status', 'start_datetime', 'is_featured', 'created')
    date_hierarchy = 'start_datetime'
    inlines = [EventURLAdminInline]

admin.site.register(Event, EventAdmin)
admin.site.register(Audience, AudienceAdmin)
