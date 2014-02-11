from django.db import models

from django_extensions.db.fields import (
    AutoSlugField, CreationDateTimeField, ModificationDateTimeField)

from us_ignite.advertising import managers


class Advert(models.Model):
    PUBLISHED = 1
    DRAFT = 2
    REMOVED = 3
    STATUS_CHOICES = (
        (PUBLISHED, 'Published'),
        (DRAFT, 'Draft'),
        (REMOVED, 'Removed'),
    )

    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    url = models.URLField(max_length=500)
    image = models.ImageField(upload_to="featured")
    is_featured = models.BooleanField(
        default=False, help_text='Marking this Advert as featured will publish'
        ' it and show it on the site.')
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    # managers:
    objects = models.Manager()
    published = managers.AdvertPublishedManager()

    class Meta:
        ordering = ('-is_featured', '-created')

    def __unicode__(self):
        return self.name
