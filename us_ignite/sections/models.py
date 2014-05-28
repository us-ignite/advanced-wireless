from django.db import models
from us_ignite.common.fields import URL_HELP_TEXT


class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(max_length=500, help_text=URL_HELP_TEXT)
    image = models.ImageField(
        upload_to="sponsor", help_text='This image is not post processed. '
        'Please make sure it has the right design specs.')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('order', )

    def __unicode__(self):
        return self.name
