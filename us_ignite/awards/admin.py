from django.contrib import admin
from us_ignite.awards.models import Award, ApplicationAward, HubAward


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
    list_filter = ('award__name',)


class UserAwardAdmin(admin.ModelAdmin):
    list_display = ('award', 'user__profile__name', 'created')
    date_hierarchy = 'created'
    list_filter = ('award__name', 'user__profile__name')
    raw_id_fields = ('user', )


admin.site.register(Award, AwardAdmin)
admin.site.register(ApplicationAward, ApplicationAwardAdmin)
admin.site.register(HubAward, HubAwardAdmin)
