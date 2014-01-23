import watson

from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from django_extensions.db.fields import (
    CreationDateTimeField, ModificationDateTimeField)
from taggit.managers import TaggableManager

from us_ignite.blog import managers, search


class Post(models.Model):
    PUBLISHED = 1
    DRAFT = 2
    REMOVED = 3
    CHOICE_STATUS = (
        (PUBLISHED, 'Published'),
        (DRAFT, 'Draft'),
        (REMOVED, 'Removed'),
    )
    status = models.IntegerField(choices=CHOICE_STATUS, default=DRAFT)
    wp_id = models.CharField(blank=True, max_length=255, editable=False)
    wp_type = models.CharField(blank=True, max_length=255, editable=False)
    wp_url = models.URLField(blank=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    content = models.TextField(blank=True)
    content_html = models.TextField(blank=True, editable=False)
    excerpt = models.TextField(blank=True)
    excerpt_html = models.TextField(blank=True, editable=False)
    author = models.ForeignKey('auth.User', blank=True, null=True)
    publication_date = models.DateTimeField(
        blank=True, null=True, default=timezone.now)
    update_date = models.DateTimeField(
        blank=True, null=True, default=timezone.now)
    tags = TaggableManager(blank=True)
    is_featured = models.BooleanField(default=False)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    # managers:
    objects = models.Manager()
    published = managers.PostPublishedManager()

    class Meta:
        get_latest_by = 'publication_date'
        ordering = ('is_featured', '-publication_date',)

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog_post_detail', args=[
            int(self.publication_date.strftime('%Y')),
            int(self.publication_date.strftime('%m')),
            self.slug
        ])

    def is_published(self):
        return (self.status == self.PUBLISHED
                and self.publication_date < timezone.now())

    def is_author(self, user):
        return self.author == user

    def is_visible_by(self, user):
        return self.is_published() or self.is_author(user)


class PostAttachment(models.Model):
    post = models.ForeignKey('blog.Post')
    wp_id = models.CharField(blank=True, max_length=255)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, blank=True)
    url = models.URLField(blank=True)
    attachment = models.FileField(upload_to='posts', blank=True)
    mime_type = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    caption = models.TextField(blank=True)

    def __unicode__(self):
        return self.title


# Search:
watson.register(
    Post.published.all(),
    search.PostSearchAdapter
)
