from django.contrib import admin
from us_ignite.smart_gigabit_communities.models import Pitch
from adminsortable2.admin import SortableAdminMixin
from tinymce.widgets import TinyMCE
from django import forms


class PitchAdminForm(forms.ModelForm):
    class Meta:
        widgets = {
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }


class PitchAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ('active', 'title', 'subtitle')
    form = PitchAdminForm


admin.site.register(Pitch, PitchAdmin)
