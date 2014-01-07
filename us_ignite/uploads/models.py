from django.db import models

from django_extensions.db.fields import (
    CreationDateTimeField, ModificationDateTimeField)


class Image(models.Model):
    title = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='uploads')
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __unicode__(self):
        return self.title


class Upload(models.Model):
    title = models.CharField(max_length=255, blank=True)
    attachment = models.FileField(upload_to='uploads')
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __unicode__(self):
        return self.title
