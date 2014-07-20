from django import forms
from django.contrib import admin

from us_ignite.snippets.models import Snippet

from tinymce.widgets import TinyMCE


class SnippetAdminForm(forms.ModelForm):

    class Meta:
        model = Snippet
        widgets = {
            'body': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }


class SnippetAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', 'url')
    list_filter = ('status', 'is_featured', 'created')
    date_hierarchy = 'created'
    form = SnippetAdminForm
    fieldsets = (
        (None, {
            'fields': ('name', 'status', 'slug', 'body')
        }),
        ('Extras', {
            'fields': ('url', 'url_text', 'image'),
        }),
    )

admin.site.register(Snippet, SnippetAdmin)
