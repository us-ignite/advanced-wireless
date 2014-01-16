from django.db import models


class ResourcePublishedManager(models.Manager):

    def get_query_set(self, *args, **kwargs):
        return (super(ResourcePublishedManager, self)
                .get_query_set(*args, **kwargs)
                .filter(status=self.model.PUBLISHED))
