from django.db import models
from django.utils import timezone


class EventPublishedManager(models.Manager):

    def get_query_set(self, *args, **kwargs):
        return (super(EventPublishedManager, self)
                .get_query_set(*args, **kwargs)
                .filter(status=self.model.PUBLISHED))

    def get_upcoming(self, **kwargs):
        return (self.get_query_set()
                .filter(start_datetime__gte=timezone.now(), **kwargs))
