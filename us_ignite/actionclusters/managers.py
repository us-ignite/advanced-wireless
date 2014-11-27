from django.db import models


class ActionClusterActiveManager(models.Manager):

    def get_query_set(self):
        return (super(ActionClusterActiveManager, self).get_query_set()
                .filter(~models.Q(status=self.model.REMOVED)))


class ActionClusterPublishedManager(models.Manager):

    def get_query_set(self):
        return (super(ActionClusterPublishedManager, self).get_query_set()
                .filter(status=self.model.PUBLISHED, is_approved=True))

    def get_featured(self):
        try:
            return (self.get_queryset().filter(is_featured=True)
                    .order_by('-is_featured', '-created')[0])
        except IndexError:
            return None

    def get_homepage(self):
        try:
            return (self.get_queryset().filter(is_homepage=True)
                    .order_by('-is_featured', '-created')[0])
        except IndexError:
            return None
