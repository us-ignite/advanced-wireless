from django.db import models

from django_extensions.db.fields import (
    CreationDateTimeField, ModificationDateTimeField)
from geoposition.fields import GeopositionField

from us_ignite.maps.managers import LocationPublishedManager


class Category(models.Model):
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255, unique=True)
    image = models.ImageField(upload_to='map', blank=True)

    def __unicode__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'categories'


class Location(models.Model):
    PUBLISHED = 1
    DRAFT = 2
    REMOVED = 3
    STATUS_CHOICES = (
        (PUBLISHED, 'Published'),
        (DRAFT, 'Draft'),
        (REMOVED, 'Removed'),
    )
    name = models.CharField(max_length=250)
    website = models.URLField(max_length=500, blank=True)
    image = models.ImageField(upload_to='map', blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    position = GeopositionField(blank=False)
    category = models.ForeignKey('maps.Category')
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    # managers:
    objects = models.Manager()
    published = LocationPublishedManager()

    def __unicode__(self):
        return self.name

    def get_image_url(self):
        if self.image:
            return self.image.url
        if self.category.image:
            return self.category.image.url
        return u''
