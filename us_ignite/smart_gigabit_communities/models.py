from django.db import models
from django_extensions.db.fields import (
    AutoSlugField, CreationDateTimeField, ModificationDateTimeField)
# Create your models here.


class Pitch(models.Model):
    active = models.BooleanField(default=False)
    title = models.CharField(max_length=255)
    subtitle = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    logo = models.ImageField(upload_to='smart_gigabit', max_length=500, blank=True, null=True)
    pitch_video = models.URLField(blank=True, null=True)
    pitch_image = models.ImageField(upload_to='smart_gigabit', max_length=500, blank=True, null=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()
    order = models.PositiveIntegerField(default=0, blank=False, null=False)

    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    google = models.URLField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    link_text = models.CharField(default="LEARN MORE", max_length=50)


    class Meta:
        ordering = ('order', )
        verbose_name_plural = "Pitches"

