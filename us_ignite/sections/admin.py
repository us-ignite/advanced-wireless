from django.contrib import admin

from us_ignite.sections.models import Sponsor, SectionPage


class SponsorAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']


class SectionPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'status']
    search_fields = ['title', 'slug', 'body', 'status', 'template']
    list_filter = ['status']

admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(SectionPage, SectionPageAdmin)
