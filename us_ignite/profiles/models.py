import hashlib

from django.db import models

from us_ignite.common.fields import AutoUUIDField
from us_ignite.profiles import managers


class Profile(models.Model):
    user = models.OneToOneField('auth.User', primary_key=True)
    slug = AutoUUIDField(unique=True)
    website = models.URLField(max_length=500, blank=True)
    bio = models.TextField(blank=True)
    # TODO: add public flag.

    # managers
    active = managers.ProfileActiveManager()
    objects = models.Manager()

    def __unicode__(self):
        return u'Profile for %s' % self.user

    @property
    def full_name(self):
        user = self.user
        return u'%s %s' % (user.first_name, user.last_name)

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
