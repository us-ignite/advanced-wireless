from django.contrib import admin

from us_ignite.testbeds.models import Testbed, NetworkSpeed


class TestbedAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created')
    search_fields = ('name', 'description', 'summary')
    date_hierarchy = 'created'
    list_filter = ('status', )


class NetworkSpeedAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

admin.site.register(Testbed, TestbedAdmin)
admin.site.register(NetworkSpeed, NetworkSpeedAdmin)
