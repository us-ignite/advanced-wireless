from django.db import models


class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(max_length=500)
    image = models.ImageField(
        upload_to="sponsor", help_text='This image is not post processed. '
        'Please make sure it has the right design specs.')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('order', )

    def __unicode__(self):
        return self.name
