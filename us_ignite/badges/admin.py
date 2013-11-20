from django.contrib import admin
from us_ignite.badges.models import Badge


class BadgeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

admin.site.register(Badge, BadgeAdmin)
