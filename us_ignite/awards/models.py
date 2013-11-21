from django.db import models
from django_extensions.db.fields import AutoSlugField, CreationDateTimeField


class Award(models.Model):
    """``Awards`` to be given."""
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    image = models.ImageField(blank=True, upload_to='awards', max_length=500)
    description = models.TextField(blank=True)

    def __unicode__(self):
        return self.name


class ApplicationAward(models.Model):
    """An award given to an application."""
    award = models.ForeignKey('awards.Award')
    application = models.ForeignKey('apps.Application')
    created = CreationDateTimeField()

    def __unicode__(self):
        return u'Award %s for %s' % (self.award, self.application)
