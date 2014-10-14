from django.db import models


class ActionClusterActiveManager(models.Manager):

    def get_query_set(self):
        return (super(ActionClusterActiveManager, self).get_query_set()
                .filter(~models.Q(status=self.model.REMOVED)))


class ActionClusterPublishedManager(models.Manager):

    def get_query_set(self):
        return (super(ActionClusterPublishedManager, self).get_query_set()
                .filter(status=self.model.PUBLISHED))

    def get_featured(self):
        try:
            return (self.get_queryset().filter(is_featured=True)
                    .order_by('-is_featured', 'created')[0])
        except IndexError:
            return None

    def get_homepage(self):
        try:
            return (self.get_queryset().filter(is_homepage=True)
                    .order_by('-is_featured', 'created')[0])
        except IndexError:
            return None


class ActionClusterVersionManager(models.Manager):

    def create_version(self, actioncluster):
        """Generates an ``ApplicationVersion`` of the given ``application``."""
        data = {
            'actioncluster': actioncluster,
            'name': actioncluster.name,
            'stage': actioncluster.stage,
            'website': actioncluster.website,
            'image': actioncluster.image,
            'summary': actioncluster.summary,
            'impact_statement': actioncluster.impact_statement,
            'assistance': actioncluster.assistance,
            'team_description': actioncluster.team_description,
            'acknowledgments': actioncluster.acknowledgments,
            'notes': actioncluster.notes,
        }
        return self.create(**data)

    def get_latest_version(self, actioncluster):
        results = self.filter(actioncluster=actioncluster).order_by('-created')
        if results:
            return results[0]
        return None