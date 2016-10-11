from django.db import models


class OrganizationActiveManager(models.Manager):

    def get_query_set(self, *args, **kwargs):
        return (super(OrganizationActiveManager, self)
                .get_queryset(*args, **kwargs)
                .filter(status=self.model.PUBLISHED))
