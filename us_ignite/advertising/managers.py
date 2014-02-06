from django.db import models


class AdvertPublishedManager(models.Manager):

    def get_query_set(self, *args, **kwargs):
        return (super(AdvertPublishedManager, self)
                .get_query_set(*args, **kwargs)
                .filter(status=self.model.PUBLISHED))
