from django.core.urlresolvers import reverse
from django.db import models

from django_extensions.db.fields import (CreationDateTimeField,
                                         ModificationDateTimeField)
from taggit.managers import TaggableManager

from us_ignite.common.fields import AutoUUIDField
from us_ignite.apps import managers


class Application(models.Model):
    PUBLISHED = 1
    DRAFT = 2
    REMOVED = 3
    PRIVATE = 4
    STATUS_CHOICES = (
        (PUBLISHED, 'Published'),
        (DRAFT, 'Draft'),
        (REMOVED, 'Removed'),
        (PRIVATE, 'Private'),
    )
    name = models.CharField(max_length=255)
    slug = AutoUUIDField(unique=True, editable=True)
    owner = models.ForeignKey('auth.User', related_name='ownership_set')
    members = models.ManyToManyField(
        'auth.User', through='apps.ApplicationMembership',
        related_name='membership_set')
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()
    description = models.TextField()
    assistance = models.TextField(blank=True)
    technology = models.TextField(blank=True)
    tags = TaggableManager(blank=True)
    # managers
    objects = models.Manager()
    active = managers.ApplicationActiveManager()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('app_detail', args=[self.slug])

    def get_edit_url(self):
        return reverse('app_edit', args=[self.slug])

    def is_public(self):
        """Verify if the ``Application`` is accessible by anyone."""
        return self.status == self.PUBLISHED

    def is_draft(self):
        """Verify if the ``Application`` is a draft."""
        return self.status == self.DRAFT

    def is_owned_by(self, user):
        """Validates if the given user owns the ``Application``."""
        return user.is_authenticated() and user.id == self.owner_id

    def has_member(self, user):
        """Validates if the given user is a member of this ``Application``."""
        return self.is_owned_by(user) or self.members.filter(pk=user.id)

    def is_visible_by(self, user):
        """Validates if this app is acessible by the given ``User``."""
        return self.is_public() or self.has_member(user)

    def is_editable_by(self, user):
        """Determines if the given user can edit the ``Application``"""
        return self.owner == user


class ApplicationMembership(models.Model):
    user = models.ForeignKey('auth.User')
    application = models.ForeignKey('apps.Application')
    created = CreationDateTimeField()

    class Meta:
        unique_together = ('user', 'application')

    def __unicode__(self):
        return (u'Membership: %s for %s'
                % (self.application.name, self.user.email))


class ApplicationURL(models.Model):
    application = models.ForeignKey('apps.Application')
    name = models.CharField(max_length=255, blank=True)
    url = models.URLField(max_length=500)

    def __unicode__(self):
        return self.url
