import watson

from django.core.urlresolvers import reverse
from django.db import models

from us_ignite.hubs import managers, search

from django_extensions.db.fields import (
    AutoSlugField, CreationDateTimeField, ModificationDateTimeField)
from taggit.managers import TaggableManager


class HubRequest(models.Model):
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
    website = models.URLField(max_length=500, blank=True)
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
        ordering = ('created', )

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


class NetworkSpeed(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __unicode__(self):
        return self.name


class Hub(models.Model):
    """Local communities with Gigabit capabilities."""
    PUBLISHED = 1
    DRAFT = 2
    STATUS_CHOICES = (
        (PUBLISHED, u'Published'),
        (DRAFT, u'Draft'),
    )
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    EXPERIMENTATION_CHOICES = (
        (LOW, u'Low'),
        (MEDIUM, u'Medium'),
        (HIGH, u'High'),
    )
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)
    summary = models.TextField(blank=True)
    description = models.TextField()
    connections = models.TextField(
        blank=True, help_text=u'Connections to other networks')
    contact = models.ForeignKey(
        'auth.User', blank=True, null=True, on_delete=models.SET_NULL)
    organization = models.ForeignKey(
        'organizations.Organization', blank=True, null=True,
        on_delete=models.SET_NULL)
    network_speed = models.ForeignKey(
        'hubs.NetworkSpeed', blank=True, null=True, on_delete=models.SET_NULL)
    is_advanced = models.BooleanField(
        default=False, help_text=u'Does it have advanced characteristics?')
    experimentation = models.IntegerField(
        choices=EXPERIMENTATION_CHOICES, default=MEDIUM,
        help_text=u'Willingness to experiment')
    estimated_passes = models.TextField(
        blank=True, help_text=u'# homes, # businesses, # community anchor '
        'institutions')
    image = models.ImageField(blank=True, upload_to='hub', max_length=500)
    website = models.URLField(max_length=500, blank=True)
    applications = models.ManyToManyField(
        'apps.Application', blank=True, help_text=u'Applications being piloted.')
    features = models.ManyToManyField(
        'apps.Feature', blank=True, help_text=u'Existing NextGen features in '
        'this community.')
    tags = TaggableManager(blank=True)
    notes = models.TextField(blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    is_featured = models.BooleanField(default=False)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    # managers
    objects = models.Manager()
    active = managers.HubActiveManager()

    class Meta:
        ordering = ('-is_featured', 'created')

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('hub_detail', args=[self.slug])

    def get_membership_url(self):
        return reverse('hub_membership', args=[self.slug])

    def get_edit_url(self):
        return reverse('hub_edit', args=[self.slug])

    def is_contact(self, user):
        return self.contact == user

    def is_published(self):
        return self.status == self.PUBLISHED

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


class HubActivity(models.Model):
    hub = models.ForeignKey('hubs.Hub')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    url = models.URLField(max_length=500, blank=True)
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

# Search:
watson.register(
    Hub.active.all(),
    search.HubSearchAdapter
)
