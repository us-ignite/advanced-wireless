from django.contrib import admin

from us_ignite.news.models import Article


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'is_featured')
    search_fields = ('name', 'url')
    list_filter = ('status', 'is_featured', 'created')
    date_hierarchy = 'created'


admin.site.register(Article, ArticleAdmin)
