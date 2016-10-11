from django.db import models


class ApplicationActiveManager(models.Manager):

    def get_query_set(self):
        return (super(ApplicationActiveManager, self).get_queryset()
                .filter(~models.Q(status=self.model.REMOVED)))


class ApplicationPublishedManager(models.Manager):

    def get_query_set(self):
        return (super(ApplicationPublishedManager, self).get_queryset()
                .filter(status=self.model.PUBLISHED))

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


class ApplicationVersionManager(models.Manager):

    def create_version(self, application):
        """Generates an ``ApplicationVersion`` of the given ``application``."""
        data = {
            'application': application,
            'name': application.name,
            'stage': application.stage,
            'website': application.website,
            'image': application.image,
            'summary': application.summary,
            'impact_statement': application.impact_statement,
            'assistance': application.assistance,
            'team_description': application.team_description,
            'acknowledgments': application.acknowledgments,
            'notes': application.notes,
        }
        return self.create(**data)

    def get_latest_version(self, application):
        results = self.filter(application=application).order_by('-created')
        if results:
            return results[0]
        return None
