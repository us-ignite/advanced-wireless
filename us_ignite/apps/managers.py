from django.db import models


class ApplicationActiveManager(models.Manager):

    def get_query_set(self):
        return (super(ApplicationActiveManager, self).get_query_set()
                .filter(~models.Q(status=self.model.REMOVED)))


class ApplicationVersionManager(models.Manager):

    def create_version(self, application):
        """Generates an ``ApplicationVersion`` of the given ``application``."""
        data = {
            'application': application,
            'name': application.name,
            'stage': application.stage,
            'image': application.image,
            'short_description': application.short_description,
            'description': application.description,
            'technology': application.technology,
            'assistance': application.assistance,
        }
        return self.create(**data)
