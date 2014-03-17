from django.db import models

from django_extensions.db.fields import (
    CreationDateTimeField, ModificationDateTimeField)

from us_ignite.news import managers


class Article(models.Model):
    PUBLISHED = 1
    DRAFT = 2
    REMOVED = 3
    STATUS_CHOICES = (
        (PUBLISHED, 'Published'),
        (DRAFT, 'Draft'),
        (REMOVED, 'Removed'),
    )

    name = models.CharField(max_length=500)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    url = models.URLField(max_length=500)
    is_featured = models.BooleanField(default=False)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    # managers:
    objects = models.Manager()
    published = managers.ArticlePublishedManager()

    class Meta:
        ordering = ('-is_featured', '-created')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return self.url
