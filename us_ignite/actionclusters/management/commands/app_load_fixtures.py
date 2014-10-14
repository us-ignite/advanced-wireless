from django.core.management.base import BaseCommand

from us_ignite.actionclusters.models import Feature, Domain


FEATURE_LIST = (
    'SDN',
    'OpenFlow',
    'Ultra fast',
    'Speed',
    'Low-latency',
    'Local cloud / edge computing',
    'Advanced wireless',
    'Ultra-fast/Gigabit to end-user',
    'GENI/US Ignite Rack',
    'Layer 2',
)

DOMAIN_LIST = (
    'Healthcare',
    'Education & Workforce',
    'Energy',
    'Transportation',
    'Advanced Manufacturing',
    'Public Safety',
    'General / Platform / Other',
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        for feature_name in FEATURE_LIST:
            feature, is_new = Feature.objects.get_or_create(name=feature_name)
            if is_new:
                print "Imported feature: %s" % feature_name
        for domain_name in DOMAIN_LIST:
            domain, is_new = Domain.objects.get_or_create(name=domain_name)
            if is_new:
                print "Imported domain: %s" % domain_name
        print "Done!"
