import hashlib

from django.db import models
from django.core.urlresolvers import reverse

from us_ignite.profiles import communications, managers
from us_ignite.common.fields import AutoUUIDField

from django_browserid.signals import user_created
from django_extensions.db.fields import (CreationDateTimeField,
                                         ModificationDateTimeField)
from registration.signals import user_activated


class Profile(models.Model):
    user = models.OneToOneField('auth.User', primary_key=True)
    slug = AutoUUIDField(unique=True, editable=True)
    name = models.CharField(max_length=255, blank=True)
    website = models.URLField(max_length=500, blank=True)
    bio = models.TextField(blank=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()
    # TODO: add status flag.

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
    def full_name(self):
        return self.name

    @property
    def display_name(self):
        return self.name if self.name else u'US Ignite user'

    @property
    def display_email(self):
        return u'%s <%s>' % (self.display_name, self.user.email)

    def get_gravatar_url(self, size=100):
        """Determines gravatar icon url"""
        user_hash = hashlib.md5(self.user.email).hexdigest()
        return u'//www.gravatar.com/avatar/%s?s=%s' % (user_hash, size)


class ProfileLink(models.Model):
    profile = models.ForeignKey('profiles.Profile')
    name = models.CharField(blank=True, max_length=255)
    url = models.URLField(max_length=500)

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
