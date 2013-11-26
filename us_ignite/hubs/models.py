from django.db import models

from django_extensions.db.fields import (
    AutoSlugField, CreationDateTimeField, ModificationDateTimeField)
from taggit.managers import TaggableManager


class Hub(models.Model):
    """Local communities with Gigabit capabilities."""
    APPROVED = 1
    PENDING = 2
    REMOVED = 3
    STATUS_CHOICES = (
        (APPROVED, 'Approved'),
        (PENDING, 'Pending'),
        (REMOVED, 'Removed'),
    )
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)
    guardian = models.ForeignKey('auth.User', blank=True, null=True)
    summary = models.TextField(blank=True)
    description = models.TextField()
    image = models.ImageField(blank=True, upload_to='hub', max_length=500)
    website = models.URLField(max_length=500, blank=True)
    features = models.ManyToManyField('apps.Feature', blank=True)
    tags = TaggableManager(blank=True)
    notes = models.TextField(blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    is_featured = models.BooleanField(default=False)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __unicode__(self):
        return self.name


class HubActivity(models.Model):
    hub = models.ForeignKey('hubs.Hub')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField(max_length=500, blank=True)
    user = models.ForeignKey('auth.User', blank=True, null=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    class Meta:
        verbose_name_plural = 'Hub Activities'

    def __unicode__(self):
        return self.name
