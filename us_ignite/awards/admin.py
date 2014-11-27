from django.contrib import admin
from us_ignite.awards.models import (
    Award,
    ActionClusterAward,
    ApplicationAward,
    HubAward,
    UserAward,
    OrganizationAward,
)


class AwardAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class ApplicationAwardAdmin(admin.ModelAdmin):
    list_display = ('award', 'application', 'created')
    date_hierarchy = 'created'
    list_filter = ('award__name',)
    raw_id_fields = ('application', )


class HubAwardAdmin(admin.ModelAdmin):
    list_display = ('award', 'hub', 'created')
    date_hierarchy = 'created'
    list_filter = ('award__name', )


class UserAwardAdmin(admin.ModelAdmin):
    list_display = ('award', 'user', 'created')
    date_hierarchy = 'created'
    list_filter = ('award__name', )
    raw_id_fields = ('user', )


class OrganizationAwardAdmin(admin.ModelAdmin):
    list_display = ('award', 'organization', 'created')
    date_hierarchy = 'created'
    list_filter = ('award__name', )
    raw_id_fields = ('organization', )


class ActionClusterAwardAdmin(admin.ModelAdmin):
    list_display = ('award', 'actioncluster', 'created')
    date_hierarchy = 'created'
    list_filter = ('award__name', )
    raw_id_fields = ('actioncluster', )


admin.site.register(Award, AwardAdmin)
admin.site.register(ActionClusterAward, ActionClusterAwardAdmin)
admin.site.register(ApplicationAward, ApplicationAwardAdmin)
admin.site.register(HubAward, HubAwardAdmin)
admin.site.register(UserAward, UserAwardAdmin)
admin.site.register(OrganizationAward, OrganizationAwardAdmin)
