from django.core.urlresolvers import reverse
from django.db import models


from django_extensions.db.fields import (CreationDateTimeField,
                                         ModificationDateTimeField)
from taggit.managers import TaggableManager

from us_ignite.common.fields import AutoUUIDField


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

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        # return reverse('app_detail', self.id)
        return '/apps/'


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
