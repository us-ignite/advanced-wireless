from django.contrib import admin

from us_ignite.snippets.models import Snippet


class SnippetAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'is_featured')
    search_fields = ('name', 'url')
    list_filter = ('status', 'is_featured', 'created')
    date_hierarchy = 'created'

    def save_model(self, request, obj, form, change):
        """Make sure that there is only a single featured ``Snippet``."""
        if obj.is_featured:
            obj.status = obj.PUBLISHED
            self.model.objects.all().update(is_featured=False)
        obj.save()

admin.site.register(Snippet, SnippetAdmin)
