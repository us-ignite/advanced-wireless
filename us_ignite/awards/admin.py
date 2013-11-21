from django.contrib import admin
from us_ignite.awards.models import Award, ApplicationAward


class AwardAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class ApplicationAwardAdmin(admin.ModelAdmin):
    list_display = ('award', 'application', 'created')
    date_hierarchy = 'created'
    list_filter = ('award__name',)

admin.site.register(Award, AwardAdmin)
admin.site.register(ApplicationAward, ApplicationAwardAdmin)
