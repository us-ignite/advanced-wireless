from django.contrib import admin
from us_ignite.awards.models import Award, ApplicationAward, HubAward


class AwardAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class ApplicationAwardAdmin(admin.ModelAdmin):
    list_display = ('award', 'application', 'created')
    date_hierarchy = 'created'
    list_filter = ('award__name',)


class HubAwardAdmin(admin.ModelAdmin):
    list_display = ('award', 'hub', 'created')
    date_hierarchy = 'created'
    list_filter = ('award__name',)


admin.site.register(Award, AwardAdmin)
admin.site.register(ApplicationAward, ApplicationAwardAdmin)
admin.site.register(HubAward, HubAwardAdmin)
