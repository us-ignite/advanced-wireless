from django.db import models

from django_extensions.db.fields import (
    CreationDateTimeField, ModificationDateTimeField)

from us_ignite.common import sanitizer
from us_ignite.snippets import managers


class Snippet(models.Model):
    PUBLISHED = 1
    DRAFT = 2
    REMOVED = 3
    STATUS_CHOICES = (
        (PUBLISHED, 'Published'),
        (DRAFT, 'Draft'),
        (REMOVED, 'Removed'),
    )
    name = models.CharField(max_length=255)
    slug = models.SlugField(
        max_length=255, unique=True, help_text='Keyword used to render this'
        ' snippet of content.')
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    body = models.TextField()
    url = models.URLField(max_length=500, blank=True)
    url_text = models.CharField(blank=True, max_length=255)
    image = models.ImageField(upload_to="featured", blank=True)
    is_featured = models.BooleanField(default=False)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    # managers:
    objects = models.Manager()
    published = managers.SnippetPublishedManager()

    class Meta:
        ordering = ('-is_featured', '-created')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.body:
            self.body = sanitizer.sanitize(self.body)
        return super(Snippet, self).save(*args, **kwargs)
