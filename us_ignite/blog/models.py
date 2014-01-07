from django.core.urlresolvers import reverse
from django.db import models
from django.utils import timezone

from django_extensions.db.fields import (
    CreationDateTimeField, ModificationDateTimeField)
from taggit.managers import TaggableManager

from us_ignite.blog import managers


class Entry(models.Model):
    PUBLISHED = 1
    DRAFT = 2
    REMOVED = 3
    CHOICE_STATUS = (
        (PUBLISHED, 'Published'),
        (DRAFT, 'Draft'),
        (REMOVED, 'Removed'),
    )
    author = models.ForeignKey('auth.User')
    publication_date = models.DateTimeField(
        blank=True, null=True, default=timezone.now)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    status = models.IntegerField(choices=CHOICE_STATUS, default=DRAFT)
    body = models.TextField()
    body_html = models.TextField()
    summary = models.TextField(blank=True)
    summary_html = models.TextField(blank=True)
    image = models.ImageField(upload_to="blog", blank=True)
    is_featured = models.BooleanField(default=False)
    tags = TaggableManager(blank=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    # managers:
    objects = models.Manager()
    published = managers.EntryPublishedManager()

    class Meta:
        get_latest_by = 'publication_date'
        ordering = ('is_featured', '-publication_date',)
        verbose_name_plural = 'Entries'

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.body_html = self.body
        if self.summary:
            self.summary_html = self.summary
        return super(Entry, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog_entry_detail', args=[
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
