from django.db import models


class ApplicationActiveManager(models.Manager):

    def get_query_set(self):
        return (super(ApplicationActiveManager, self).get_query_set()
                .filter(~models.Q(status=self.model.REMOVED)))
