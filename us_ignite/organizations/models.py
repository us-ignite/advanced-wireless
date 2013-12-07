from django.db import models

from django_extensions.db.fields import (
    CreationDateTimeField, ModificationDateTimeField)
from taggit.managers import TaggableManager


class Organization(models.Model):
    PUBLISHED = 1
    DRAFT = 2
    REMOVED = 3
    STATUS_CHOICES = (
        (PUBLISHED, 'Published'),
        (DRAFT, 'Draft'),
        (REMOVED, 'Removed'),
    )
    name = models.CharField(max_length=250)
    slug = models.SlugField(max_length=255)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to="org", blank=True)
    members = models.ManyToManyField(
        'auth.User', blank=True, through='organizations.OrganizationMember')
    tags = TaggableManager(blank=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __unicode__(self):
        return self.name

    def is_published(self):
        return self.status == self.PUBLISHED

    def is_draft(self):
        return self.status == self.DRAFT

    def is_member(self, user):
        return True if self.members.filter(id__exact=user.id) else False

    def is_visible_by(self, user):
        return self.is_published() or self.is_member(user)


class OrganizationMember(models.Model):
    user = models.ForeignKey('auth.User')
    organization = models.ForeignKey('organizations.Organization')
    created = CreationDateTimeField()

    def __unicode__(self):
        return u'%s membership of %s' % (self.organization, self.user)
