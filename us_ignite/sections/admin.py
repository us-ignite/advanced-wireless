from django import forms
from django.contrib import admin

from us_ignite.sections.models import Sponsor, SectionPage

from tinymce.widgets import TinyMCE


class SectionPageForm(forms.ModelForm):

    class Meta:
        model = SectionPage
        widgets = {
            'body': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }


class SponsorAdmin(admin.ModelAdmin):
    list_display = ['name', 'order']


class SectionPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'status']
    search_fields = ['title', 'slug', 'body', 'status', 'template']
    list_filter = ['status', 'section']
    form = SectionPageForm

admin.site.register(Sponsor, SponsorAdmin)
admin.site.register(SectionPage, SectionPageAdmin)
