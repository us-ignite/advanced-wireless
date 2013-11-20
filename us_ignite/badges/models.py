from django.db import models
from django_extensions.db.fields import AutoSlugField, CreationDateTimeField


class Badge(models.Model):
    """``Badges`` to be awarded"""
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    image = models.ImageField(blank=True, upload_to='badges', max_length=500)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class ApplicationBadge(models.Model):
    """A badge awarded to an application."""
    badge = models.ForeignKey('badges.Badge')
    application = models.ForeignKey('apps.Application')
    created = CreationDateTimeField()

    def __unicode__(self):
        return u'Badge %s for %s' % (self.badge, self.application)
