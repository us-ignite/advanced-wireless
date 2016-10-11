from django.db import models


class ArticlePublishedManager(models.Manager):

    def get_query_set(self, *args, **kwargs):
        return (super(ArticlePublishedManager, self)
                .get_queryset(*args, **kwargs)
                .filter(status=self.model.PUBLISHED))
