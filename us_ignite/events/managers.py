from django.db import models


class EventPublishedManager(models.Manager):

    def get_query_set(self, *args, **kwargs):
        return (super(EventPublishedManager, self)
                .get_query_set(*args, **kwargs)
                .filter(status=self.model.PUBLISHED))
