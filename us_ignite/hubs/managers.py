from django.db import models


class HubActiveManager(models.Manager):

    def get_query_set(self, *args, **kwargs):
        return (super(HubActiveManager, self).get_queryset(*args, **kwargs)
                .filter(status=self.model.PUBLISHED))

    def get_featured(self):
        try:
            return (self.get_query_set().filter(is_featured=True).
                    order_by('-is_featured', '-created')[0])
        except IndexError:
            return None

    def get_homepage(self):
        try:
            return (self.get_query_set().filter(is_homepage=True).
                    order_by('-is_featured', '-created')[0])
        except IndexError:
            return None
