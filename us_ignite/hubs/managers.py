from django.db import models


class HubActiveManager(models.Manager):

    def get_query_set(self, *args, **kwargs):
        return (super(HubActiveManager, self)
                .get_query_set(*args, **kwargs)
                .filter(status=self.model.PUBLISHED))
