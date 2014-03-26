from django.core.management.base import BaseCommand

from us_ignite.resources.models import ResourceType, Sector


RESOURCE_LIST = (
    'Funding Opportunity',
    'Video',
    'Presentation',
    'Tool',
    'Testbed',
    'External Group',
    'Other',
)

SECTOR_LIST = (
    'Healthcare',
    'Education & Workforce development',
    'Energy',
    'Transportation',
    'Advanced Manufacturing',
    'Public Safety',
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        for resource_name in RESOURCE_LIST:
            resource, is_new = (ResourceType.objects
                                .get_or_create(name=resource_name))
            if is_new:
                print "Imported resource type: %s" % resource_name
        for sector_name in SECTOR_LIST:
            sector, is_new = Sector.objects.get_or_create(name=sector_name)
            if is_new:
                print "Imported sector: %s" % sector_name
