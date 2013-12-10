from django.db import models
from django.utils import timezone


class ActiveChallenges(models.Manager):

    def get_query_set(self, *args, **kwargs):
        now = timezone.now()
        return (super(ActiveChallenges, self)
                .get_query_set(*args, **kwargs)
                .filter(start_datetime__lte=now,
                        end_datetime__gte=now, status=self.model.PUBLISHED))
