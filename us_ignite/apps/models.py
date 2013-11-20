from django.core.urlresolvers import reverse
from django.db import models

from django_extensions.db.fields import (
    AutoSlugField, CreationDateTimeField, ModificationDateTimeField)
from taggit.managers import TaggableManager

from us_ignite.common.fields import AutoUUIDField
from us_ignite.common.text import truncatewords
from us_ignite.apps import managers


class Feature(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')

    def __unicode__(self):
        return self.name


class Domain(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')

    def __unicode__(self):
        return self.name


class ApplicationBase(models.Model):
    """Abstract model for ``Application`` and ``ApplicationVersion`` fields."""
    IDEA = 1
    TEAM = 2
    ALPHA = 3
    BETA = 4
    DEMO = 5
    DEPLOYABLE = 6
    STAGE_CHOICES = (
        (IDEA, 'Idea complete'),
        (TEAM, 'Team complete / Forming team'),
        (ALPHA, 'Alpha version / developing alpha / testing alpha.'),
        (BETA, 'Beta version / developing beta / in beta test'),
        (DEMO, 'Demo-able / demoing'),
        (DEPLOYABLE, 'Deployable / deploying')
    )
    name = models.CharField(max_length=255)
    stage = models.IntegerField(choices=STAGE_CHOICES, default=IDEA)
    website = models.URLField(max_length=500)
    image = models.ImageField(blank=True, upload_to='apps', max_length=500)
    summary = models.TextField(
        blank=True, help_text='Tweet-length pitch summary of project.')
    impact_statement = models.TextField(
        blank=True, help_text='Story of benefit.')
    description = models.TextField()
    roadmap = models.TextField(blank=True, help_text='Development Roadmap.')
    assistance = models.TextField(
        blank=True, help_text='Fill in this field if you require help.')
    team_description = models.TextField(blank=True)
    acknowledgments = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    class Meta:
        abstract = True


class Application(ApplicationBase):
    """``Applications``add core

    Any content related field that needs to be versioned must be
    added to the ``ApplicationBase``"""
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
    slug = AutoUUIDField(unique=True, editable=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    is_featured = models.BooleanField(default=False)
    owner = models.ForeignKey('auth.User', related_name='ownership_set')
    members = models.ManyToManyField(
        'auth.User', through='apps.ApplicationMembership',
        related_name='membership_set')
    features = models.ManyToManyField('apps.Feature', blank=True)
    domain = models.ForeignKey('apps.Domain', blank=True, null=True)
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

    def get_version_url(self):
        return reverse('app_version_add', args=[self.slug])

    def get_membership_url(self):
        return reverse('app_membership', args=[self.slug])

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

    def get_summary(self):
        if self.summary:
            return self.summary
        return truncatewords(self.description, 30)


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


class ApplicationImage(models.Model):
    application = models.ForeignKey('apps.Application')
    name = models.CharField(max_length=255, blank=True)
    image = models.ImageField(blank=True, upload_to='apps', max_length=500)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __unicode__(self):
        return 'Image: %s' % self.name


class ApplicationVersion(ApplicationBase):
    """Version of the ``Application``."""
    application = models.ForeignKey('apps.Application')
    slug = AutoUUIDField(unique=True, editable=True)
    # managers:
    objects = managers.ApplicationVersionManager()

    def __unicode__(self):
        return u'Version %s of application' % self.application

    def get_absolute_url(self):
        return reverse(
            'app_version_detail', args=[self.application.slug, self.slug])
