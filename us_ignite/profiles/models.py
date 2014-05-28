import watson

import hashlib

from django.db import models
from django.core.urlresolvers import reverse

from us_ignite.profiles import communications, managers, search
from us_ignite.common.fields import AutoUUIDField, URL_HELP_TEXT

from django_browserid.signals import user_created
from django_extensions.db.fields import (
    AutoSlugField,
    CreationDateTimeField,
    ModificationDateTimeField,
)
from geoposition.fields import GeopositionField
from taggit.managers import TaggableManager
from registration.signals import user_activated


class Interest(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name', )


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ('name', )


class Profile(models.Model):
    NO_AVAILABILITY = 0
    LIMITED_AVAILABILITY = 1
    MODERATE_AVAILABILITY = 2
    HIGH_AVAILABILITY = 3
    AVAILABILITY_CHOICES = (
        (NO_AVAILABILITY, u'I do not have any availability at this time'),
        (LIMITED_AVAILABILITY, u'I have limited availability'),
        (MODERATE_AVAILABILITY, u'I might be available'),
        (HIGH_AVAILABILITY, u'Yes, I would love to join a project'),
    )
    user = models.OneToOneField('auth.User', primary_key=True)
    slug = AutoUUIDField(unique=True, editable=True)
    website = models.URLField(
        max_length=500, blank=True, help_text=URL_HELP_TEXT)
    quote = models.TextField(
        blank=True, max_length=140, help_text=u'Short quote.')
    bio = models.TextField(blank=True)
    skills = models.TextField(
        blank=True, help_text=u'What do you have to contribute? '
        'Design skills? Programming languages? Subject matter expertise?'
        ' Project management experience?')
    availability = models.IntegerField(
        choices=AVAILABILITY_CHOICES, default=NO_AVAILABILITY)
    interests = models.ManyToManyField('profiles.Interest', blank=True)
    interests_other = models.CharField(blank=True, max_length=255)
    category = models.ForeignKey(
        'profiles.Category', blank=True, null=True,
        verbose_name=u'I associate most with')
    category_other = models.CharField(blank=True, max_length=255)
    position = GeopositionField(blank=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()
    tags = TaggableManager(blank=True)
    is_public = models.BooleanField(
        default=False, help_text='By marking the profile as public it will be'
        ' shown in search results.')

    # managers
    objects = models.Manager()
    active = managers.ProfileActiveManager()

    def __unicode__(self):
        return u'Profile for %s' % self.user

    def get_absolute_url(self):
        return reverse('profile_detail', args=[self.slug])

    def get_delete_url(self):
        return reverse('user_profile_delete')

    def get_contact_url(self):
        return reverse('contact_user', args=[self.slug])

    @property
    def name(self):
        user = self.user
        if user.first_name or user.last_name:
            name = user.first_name
            if user.first_name and user.last_name:
                name += u' '
            name += user.last_name
            return name
        return u''

    @property
    def full_name(self):
        return self.name

    @property
    def display_name(self):
        return self.name if self.name else u'US Ignite user'

    @property
    def display_email(self):
        return u'%s <%s>' % (self.display_name, self.user.email)

    def get_gravatar_url(self, size=276):
        """Determines gravatar icon url"""
        user_hash = hashlib.md5(self.user.email).hexdigest()
        return u'//www.gravatar.com/avatar/%s?s=%s' % (user_hash, size)

    def is_owned_by(self, user):
        return self.user == user


class ProfileLink(models.Model):
    profile = models.ForeignKey('profiles.Profile')
    name = models.CharField(blank=True, max_length=255)
    url = models.URLField(
        max_length=500, help_text=URL_HELP_TEXT, verbose_name=u'URL')

    def __unicode__(self):
        return u'Profile link.'

    @models.permalink
    def get_absolute_url(self):
        return self.url


# Mozilla persona flow:
# Welcome email when a new account is created:
user_created.connect(
    communications.send_welcome_email, dispatch_uid='browserid_welcome_email')
# Create a profile on new account creation:
user_created.connect(
    Profile.active.get_or_create_for_user,
    dispatch_uid='browserid_create_profile')

# US Ignite registration flow:
# Welcome email when new account is created:
user_activated.connect(
    communications.send_welcome_email, dispatch_uid='registration_welcome_email')
user_activated.connect(
    Profile.active.get_or_create_for_user,
    dispatch_uid='registration_create_profile')

# Search:
watson.register(
    Profile.objects.filter(is_public=True, user__is_active=True),
    search.ProfileSearchAdapter
)
