from django.db import models


class TestbedActiveManager(models.Manager):

    def get_query_set(self, *args, **kwargs):
        return (super(TestbedActiveManager, self).get_query_set(*args, **kwargs)
                .filter(status=self.model.PUBLISHED))
