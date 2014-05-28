from django.core.urlresolvers import reverse
from django.db import models

from us_ignite.common.fields import URL_HELP_TEXT
from us_ignite.testbeds import managers

from geoposition.fields import GeopositionField
from django_extensions.db.fields import (
    AutoSlugField, CreationDateTimeField, ModificationDateTimeField)
from taggit.managers import TaggableManager


class NetworkSpeed(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __unicode__(self):
        return self.name


class Testbed(models.Model):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    EXPERIMENTATION_CHOICES = (
        (LOW, u'Low'),
        (MEDIUM, u'Medium'),
        (HIGH, u'High'),
    )
    PUBLISHED = 1
    DRAFT = 2
    STATUS_CHOICES = (
        (PUBLISHED, u'Published'),
        (DRAFT, u'Draft'),
    )
    name = models.CharField(
        max_length=255, verbose_name=u'Name of the Testbed')
    slug = AutoSlugField(populate_from='name', unique=True)
    summary = models.TextField(blank=True)
    description = models.TextField()
    contact = models.ForeignKey(
        'auth.User', blank=True, null=True, on_delete=models.SET_NULL)
    organization = models.ForeignKey(
        'organizations.Organization', blank=True, null=True,
        on_delete=models.SET_NULL)
    website = models.URLField(
        max_length=500, blank=True, help_text=URL_HELP_TEXT)
    image = models.ImageField(blank=True, upload_to='testbed', max_length=500)
    network_speed = models.ForeignKey(
        'testbeds.NetworkSpeed', blank=True, null=True,
        on_delete=models.SET_NULL)
    connections = models.TextField(
        blank=True, verbose_name=u'Connections to other networks')
    experimentation = models.IntegerField(
        choices=EXPERIMENTATION_CHOICES, default=MEDIUM,
        verbose_name=u'Willingness to experiment')
    passes_homes = models.PositiveIntegerField(
        default=0, verbose_name=u'Estimated passes # homes')
    passes_business = models.PositiveIntegerField(
        default=0, verbose_name=u'Estimated passes # business')
    passes_anchor = models.PositiveIntegerField(
        default=0, verbose_name=u'Estimated passes # community anchor')
    is_advanced = models.BooleanField(
        default=False, help_text=u'Does it have advanced characteristics?')
    applications = models.ManyToManyField(
        'apps.Application', blank=True, verbose_name=u'Applications being '
        'piloted')
    features = models.ManyToManyField(
        'apps.Feature', blank=True, help_text=u'Existing NextGen features in '
        'this community.')
    position = GeopositionField(blank=True)
    tags = TaggableManager(blank=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    # Managers:
    objects = models.Manager()
    active = managers.TestbedActiveManager()

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('testbed_detail', args=[self.slug])

    def get_edit_url(self):
        return reverse('admin:testbeds_testbed_change', args=[self.pk])

    def is_contact(self, user):
        return self.contact == user

    def is_published(self):
        return self.status == self.PUBLISHED

    def is_draft(self):
        return self.status == self.DRAFT

    def is_visible_by(self, user):
        return self.is_published() or self.is_contact(user)

    def is_editable_by(self, user):
        """Only editable in the admin section."""
        return user and user.is_superuser
