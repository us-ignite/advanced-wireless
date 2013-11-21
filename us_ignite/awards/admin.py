from django.contrib import admin
from us_ignite.awards.models import Award


class AwardAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

admin.site.register(Award, AwardAdmin)
