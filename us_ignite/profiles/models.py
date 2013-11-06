import hashlib

from django.db import models
from django.core.urlresolvers import reverse

from us_ignite.profiles import communications, managers
from us_ignite.common.fields import AutoUUIDField

from django_browserid.signals import user_created
from registration.signals import user_activated


class Profile(models.Model):
    user = models.OneToOneField('auth.User', primary_key=True)
    slug = AutoUUIDField(unique=True, editable=True)
    name = models.CharField(max_length=255, blank=True)
    website = models.URLField(max_length=500, blank=True)
    bio = models.TextField(blank=True)
    # TODO: add public flag.

    # managers
    objects = models.Manager()
    active = managers.ProfileActiveManager()

    def __unicode__(self):
        return u'Profile for %s' % self.user

    @property
    def full_name(self):
        return self.name

    def get_gravatar_url(self, size=100):
        """Determines gravatar icon url"""
        user_hash = hashlib.md5(self.user.email).hexdigest()
        return u'//www.gravatar.com/avatar/%s?s=%s' % (user_hash, size)

    def get_absolute_url(self):
        return reverse('profile_detail', args=[self.slug])


class ProfileLink(models.Model):
    profile = models.ForeignKey('profiles.Profile')
    name = models.CharField(blank=True, max_length=255)
    url = models.URLField(max_length=500)

    def __unicode__(self):
        return u'Profile link.'

    @models.permalink
    def get_absolute_url(self):
        return self.url


# Welcome email when a new account is created via Mozilla Persona:
user_created.connect(
    communications.send_welcome_email, dispatch_uid='browserid_welcome_email')

# Welcome email when a user has been activated via US Ignite registration:
user_activated.connect(
    communications.send_welcome_email, dispatch_uid='registration_welcome_email')
