import watson

from django.core.urlresolvers import reverse
from django.db import models

from us_ignite.constants import IMAGE_HELP_TEXT
from us_ignite.common.fields import URL_HELP_TEXT
from us_ignite.hubs import managers

from geoposition.fields import GeopositionField
from django_extensions.db.fields import (
    AutoSlugField, CreationDateTimeField, ModificationDateTimeField)
from taggit.managers import TaggableManager


class HubRequest(models.Model):
    """User Requests to be a Ignite Community."""
    APPROVED = 1
    PENDING = 2
    REJECTED = 3
    REMOVED = 4
    STATUS_CHOICES = (
        (APPROVED, 'Approved'),
        (PENDING, 'Pending'),
        (REJECTED, 'Rejected'),
        (REMOVED, 'Removed'),
    )
    name = models.CharField(max_length=255)
    hub = models.ForeignKey('hubs.Hub', blank=True, null=True)
    website = models.URLField(
        max_length=500, blank=True, help_text=URL_HELP_TEXT)
    summary = models.TextField(blank=True)
    description = models.TextField()
    user = models.ForeignKey('auth.User')
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    notes = models.TextField(
        blank=True, help_text='These notes will be feedback to the applicant.')
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __unicode__(self):
        return u'%s by %s' % (self.name, self.user)

    class Meta:
        ordering = ('-created', )

    def get_admin_url(self):
        return reverse('admin:hubs_hubrequest_change', args=[self.id])

    def is_approved(self):
        return self.status == self.APPROVED

    def is_rejected(self):
        return self.status == self.REJECTED

    def is_removed(self):
        return self.status == self.REMOVED

    def is_pending(self):
        return (self.status == self.PENDING) and not self.hub


class Hub(models.Model):
    """Local communities with Gigabit capabilities."""
    PUBLISHED = 1
    DRAFT = 2
    STATUS_CHOICES = (
        (PUBLISHED, u'Published'),
        (DRAFT, u'Draft'),
    )
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)
    summary = models.TextField(blank=True)
    description = models.TextField()
    contact = models.ForeignKey(
        'auth.User', blank=True, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(blank=True, upload_to='hub', max_length=500,
                              help_text=IMAGE_HELP_TEXT)
    website = models.URLField(
        max_length=500, blank=True, help_text=URL_HELP_TEXT)
    features = models.ManyToManyField(
        'apps.Feature', blank=True, help_text=u'Existing NextGen features in '
        'this community.')
    position = GeopositionField(blank=True)
    tags = TaggableManager(blank=True)
    notes = models.TextField(blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    is_homepage = models.BooleanField(
        default=False, verbose_name='Show in the homepage?',
        help_text=u'If marked this element will be shown in the homepage.')
    is_featured = models.BooleanField(default=False)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    # managers
    objects = models.Manager()
    active = managers.HubActiveManager()

    class Meta:
        ordering = ('-is_featured', '-created')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Replace any previous homepage item when published:
        if self.is_homepage and self.is_published():
            self.__class__.objects.all().update(is_homepage=False)
        return super(Hub, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('hub_detail', args=[self.slug])

    def get_membership_url(self):
        return reverse('hub_membership', args=[self.slug])

    def get_membership_remove_url(self):
        return reverse('hub_membership_remove', args=[self.slug])

    def get_edit_url(self):
        return reverse('hub_edit', args=[self.slug])

    def is_contact(self, user):
        return self.contact == user

    def is_published(self):
        return self.status == self.PUBLISHED

    def is_draft(self):
        return self.status == self.DRAFT

    def is_visible_by(self, user):
        return self.is_published() or self.is_contact(user)

    def record_activity(self, name, extra_data=None):
        data = {
            'hub': self,
            'name': name,
        }
        if extra_data:
            data.update(extra_data)
        return HubActivity.objects.create(**data)

    @property
    def owner(self):
        return self.contact


class HubURL(models.Model):
    hub = models.ForeignKey('hubs.Hub')
    name = models.CharField(max_length=255, blank=True)
    url = models.URLField(
        max_length=500, verbose_name=u'URL', help_text=URL_HELP_TEXT)

    def __unicode__(self):
        return self.url


class HubActivity(models.Model):
    hub = models.ForeignKey('hubs.Hub')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField(
        max_length=500, blank=True, verbose_name=u'URL',
        help_text=URL_HELP_TEXT)
    user = models.ForeignKey('auth.User', blank=True, null=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    class Meta:
        verbose_name_plural = 'hub activities'
        ordering = ('-created', )

    def __unicode__(self):
        return self.name


class HubMembership(models.Model):
    hub = models.ForeignKey('hubs.Hub')
    user = models.ForeignKey('auth.User')
    created = CreationDateTimeField()

    class Meta:
        ordering = ('-created', )


class HubAppMembership(models.Model):
    hub = models.ForeignKey('hubs.Hub')
    application = models.ForeignKey('apps.Application')
    is_featured = models.BooleanField(default=False)
    created = CreationDateTimeField()

    class Meta:
        ordering = ('-created', )


class HubActionClusterMembership(models.Model):
    hub = models.ForeignKey('hubs.Hub')
    actioncluster = models.ForeignKey('actionclusters.ActionCluster')
    is_featured = models.BooleanField(default=False)
    created = CreationDateTimeField()

    class Meta:
        ordering = ('-created', )

# # Search:
# watson.register(
#     Hub.active.all(),
#     search.HubSearchAdapter
# )
