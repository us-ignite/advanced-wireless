from django.db import models

from django_extensions.db.fields import (
    CreationDateTimeField, ModificationDateTimeField)

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
    url = models.URLField(max_length=500)
    url_text = models.CharField(blank=True, max_length=255)
    body = models.TextField(blank=True)
    image = models.ImageField(upload_to="featured", blank=True)
    is_featured = models.BooleanField(
        default=False, help_text='Marking this Snippet as featured will publish'
        ' it and show it on the site.')
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    # managers:
    objects = models.Manager()
    published = managers.SnippetPublishedManager()

    class Meta:
        ordering = ('-is_featured', '-created')

    def __unicode__(self):
        return self.name
