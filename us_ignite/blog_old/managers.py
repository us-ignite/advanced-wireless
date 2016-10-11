from django.db import models
from django.utils import timezone


class PostPublishedManager(models.Manager):

    def get_query_set(self, *args, **kwargs):
        return (super(PostPublishedManager , self)
                .get_queryset(*args, **kwargs)
                .filter(status=self.model.PUBLISHED,
                        publication_date__lte=timezone.now()))
