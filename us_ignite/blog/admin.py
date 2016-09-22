from django import forms
from django.contrib import admin
from django.contrib.auth.models import User

from us_ignite.common import sanitizer
from us_ignite.blog.models import BlogLink, Post, PostAttachment

from tinymce.widgets import TinyMCE


class PostAdminForm(forms.ModelForm):
    author = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=True), required=False)

    def clean_content(self):
        if 'content' in self.cleaned_data:
            return sanitizer.sanitize(self.cleaned_data['content'])

    class Meta:
        model = Post
        widgets = {
            'content': TinyMCE(attrs={'cols': 80, 'rows': 30}),
        }
        fields = '__all__'


class PostAttachmentInline(admin.StackedInline):
    model = PostAttachment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'is_published', 'is_featured', 'status')
    list_filter = ('status', 'publication_date')
    search_fields = ('slug', 'title', 'content', 'excerpt')
    date_hierarchy = 'publication_date'
    prepopulated_fields = {'slug': ('title',)}
    form = PostAdminForm
    inlines = [PostAttachmentInline]


class BlogLinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url')
    search_fields = ('name', 'url')
    list_filter = ('created', )
    date_hierarchy = 'created'


admin.site.register(Post, PostAdmin)
admin.site.register(BlogLink, BlogLinkAdmin)
