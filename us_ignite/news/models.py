from django.db import models

from django_extensions.db.fields import (
    CreationDateTimeField, ModificationDateTimeField)

from us_ignite.common.fields import URL_HELP_TEXT
from us_ignite.news import managers


class Article(models.Model):
    PUBLISHED = 1
    DRAFT = 2
    REMOVED = 3
    STATUS_CHOICES = (
        (PUBLISHED, u'Published'),
        (DRAFT, u'Draft'),
        (REMOVED, u'Removed'),
    )
    DEFAULT = 1
    GLOBALCITIES = 2
    TYPE_CHOICES = (
        (DEFAULT, u'Default'),
        (GLOBALCITIES, u'Global Cities'),
    )
    name = models.CharField(max_length=500)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    article_type = models.IntegerField(choices=TYPE_CHOICES, default=DEFAULT)
    url = models.URLField(
        max_length=500, help_text=URL_HELP_TEXT, verbose_name=u'URL')
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
