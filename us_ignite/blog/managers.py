from django.db import models
from django.utils import timezone


class EntryPublishedManager(models.Manager):

    def get_query_set(self, *args, **kwargs):
        return (super(EntryPublishedManager , self)
            .get_query_set(*args, **kwargs)
                .filter(status=self.model.PUBLISHED,
                        publication_date__lte=timezone.now()))
