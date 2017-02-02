from django.contrib import admin
from us_ignite.smart_gigabit_communities.models import Pitch
from adminsortable2.admin import SortableAdminMixin

# Register your models here.


class PitchAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('active', 'title', 'subtitle')

    class Meta:
        verbose_name_plural = "Pitches"


admin.site.register(Pitch, PitchAdmin)
