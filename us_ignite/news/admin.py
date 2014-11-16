from django import forms
from django.contrib import admin

from us_ignite.news.models import Article


class ArticleAdminForm(forms.ModelForm):
    class Meta:
        fields = ('name', 'status', 'url', 'section', 'is_featured')
        model = Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'is_featured')
    search_fields = ('name', 'url')
    list_filter = ('status', 'is_featured', 'created')
    date_hierarchy = 'created'
    form = ArticleAdminForm

    def queryset(self, request):
        """Return DEFAULT ``News`` only."""
        return (super(ArticleAdmin, self).queryset(request)
                .filter(section=self.model.DEFAULT))


admin.site.register(Article, ArticleAdmin)
