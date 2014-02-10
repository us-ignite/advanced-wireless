from django.contrib import admin

from us_ignite.sections.models import Sponsor


class SponsorAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']


admin.site.register(Sponsor, SponsorAdmin)
