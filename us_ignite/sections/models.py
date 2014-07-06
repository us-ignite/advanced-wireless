from django.db import models

from django_extensions.db.fields import AutoSlugField, CreationDateTimeField
from us_ignite.common.fields import URL_HELP_TEXT


class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(max_length=500, help_text=URL_HELP_TEXT)
    image = models.ImageField(
        upload_to="sponsor", help_text='This image is not post processed. '
        'Please make sure it has the right design specs.')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('order', )

    def __unicode__(self):
        return self.name


class SectionPage(models.Model):
    """Describes static Pages"""
    PUBLISHED = 1
    DRAFT = 2
    REMOVED = 3
    STATUS_CHOICES = (
        (PUBLISHED, 'Published'),
        (DRAFT, 'Draft'),
        (REMOVED, 'Removed'),
    )
    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True)
    body = models.TextField(blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PUBLISHED)
    template = models.CharField(max_length=500, blank=True)
    created = CreationDateTimeField()

    def __unicode__(self):
        return self.title
