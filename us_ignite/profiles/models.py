from django.db import models

from us_ignite.profiles import managers


class Profile(models.Model):
    user = models.OneToOneField('auth.User', primary_key=True)
    website = models.URLField(max_length=500, blank=True)
    bio = models.TextField(blank=True)
    # TODO: add public flag.

    # managers
    active = managers.ProfileActiveManager()
    objects = models.Manager()

    def __unicode__(self):
        return u'Profile for %s' % self.user


class ProfileLink(models.Model):
    profile = models.ForeignKey('profiles.Profile')
    name = models.CharField(blank=True, max_length=255)
    url = models.URLField(max_length=500)

    def __unicode__(self):
        return u'Profile link.'

    @models.permalink
    def get_absolute_url(self):
        return self.url
