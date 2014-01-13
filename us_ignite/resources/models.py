from django.core.urlresolvers import reverse
from django.db import models

from us_ignite.common.fields import AutoUUIDField

from django_extensions.db.fields import (
    CreationDateTimeField, ModificationDateTimeField)
from taggit.managers import TaggableManager


class Resource(models.Model):
    PUBLISHED = 1
    DRAFT = 2
    REMOVED = 3
    STATUS_CHOICES = (
        (PUBLISHED, 'Published'),
        (DRAFT, 'Draft'),
        (REMOVED, 'Removed'),
    )
    name = models.CharField(max_length=255)
    slug = AutoUUIDField(unique=True, editable=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    description = models.TextField()
    owner = models.ForeignKey('auth.User')
    organization = models.ForeignKey(
        'organizations.Organization', blank=True, null=True)
    url = models.URLField(max_length=500, blank=True)
    asset = models.ImageField(upload_to="resource", blank=True)
    is_featured = models.BooleanField(default=False)
    tags = TaggableManager(blank=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    class Meta:
        ordering = ('-is_featured', '-created')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('resource_detail', args=[self.slug])

    def get_resource_url(self):
        if self.asset:
            return self.asset.url
        if self.url:
            return self.url
        return u''

    def is_visible_by(self, user):
        return self.is_published() or self.is_owner(user)

    def is_owner(self, user):
        return user == self.owner

    def is_published(self):
        return self.status == self.PUBLISHED
