from django.contrib import admin

from us_ignite.actionclusters.models import ActionCluster


class ActionClusterAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created')
    search_fields = ('name', 'description', 'summary')
    date_hierarchy = 'created'
    list_filter = ('status', )

admin.site.register(ActionCluster, ActionClusterAdmin)