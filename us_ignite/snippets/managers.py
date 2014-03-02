from django.db import models


class SnippetPublishedManager(models.Manager):

    def get_query_set(self, *args, **kwargs):
        return (super(SnippetPublishedManager, self)
                .get_query_set(*args, **kwargs)
                .filter(status=self.model.PUBLISHED))

    def get_featured(self):
        try:
            return (self.get_query_set().filter(is_featured=True)[0])
        except IndexError:
            return None

    def get_from_key(self, key):
        try:
            return self.get_query_set().get(slug=key)
        except self.model.DoesNotExist:
            return None
