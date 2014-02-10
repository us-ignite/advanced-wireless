from django.db import models


class Sponsor(models.Model):
    name = models.CharField(max_length=255)
    website = models.URLField(max_length=500)
    image = models.ImageField(upload_to="sponsor")
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('order', )

    def __unicode__(self):
        return self.name
