from django import forms
from django.contrib import admin
from django.contrib.auth.models import User

from us_ignite.blog.models import Post


class PostAdminForm(forms.ModelForm):
    author = forms.ModelChoiceField(
        queryset=User.objects.filter(is_superuser=True))

    class Meta:
        model = Post


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'is_featured', 'status')
    list_filter = ('status', 'publication_date')
    search_fields = ('slug', 'title', 'body', 'summary')
    date_hierarchy = 'publication_date'
    prepopulated_fields = {'slug': ('title',)}
    form = PostAdminForm


admin.site.register(Post, PostAdmin)