import watson

from django.core.urlresolvers import reverse
from django.db import models

from us_ignite.common.fields import AutoUUIDField
from us_ignite.resources import managers, search

from django_extensions.db.fields import (
    AutoSlugField,
    CreationDateTimeField,
    ModificationDateTimeField,
)
from taggit.managers import TaggableManager


class ResourceType(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __unicode__(self):
        return self.name


class Sector(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __unicode__(self):
        return self.name


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
    url = models.URLField(max_length=500, blank=True)
    description = models.TextField()
    resource_type = models.ForeignKey(
        'resources.ResourceType', blank=True, null=True,
        on_delete=models.SET_NULL)
    sector = models.ForeignKey(
        'resources.Sector', blank=True, null=True, on_delete=models.SET_NULL)
    contact = models.ForeignKey(
        'auth.User', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='resource_contact_set')
    author = models.ForeignKey(
        'auth.User', blank=True, null=True, on_delete=models.SET_NULL,
        related_name='resource_author_set')
    organization = models.ForeignKey(
        'organizations.Organization', blank=True, null=True,
        on_delete=models.SET_NULL)
    image = models.ImageField(upload_to="resource", blank=True)
    asset = models.FileField(upload_to="resource", blank=True)
    is_featured = models.BooleanField(default=False)
    tags = TaggableManager(blank=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    # Managers
    objects = models.Manager()
    published = managers.ResourcePublishedManager()

    class Meta:
        ordering = ('-is_featured', '-created')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('resource_detail', args=[self.slug])

    def get_edit_url(self):
        return reverse('resource_edit', args=[self.slug])

    def get_resource_url(self):
        if self.asset:
            return self.asset.url
        if self.url:
            return self.url
        return u''

    def is_visible_by(self, user):
        return self.is_published() or self.is_editable_by(user)

    def is_editable_by(self, user):
        return self.contact and (user == self.contact)

    def is_published(self):
        return self.status == self.PUBLISHED

    def is_draft(self):
        return self.status == self.DRAFT


# Search:
watson.register(
    Resource.published.all(),
    search.ResourceSearchAdapter
)
