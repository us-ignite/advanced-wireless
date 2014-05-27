from django.core.management.base import BaseCommand

from us_ignite.testbeds.models import NetworkSpeed


SPEED_LIST = (
    '100 Mbps symmetric or higher',
    '200 Mbps symmetric or higher',
    '1 Gbps symmetric or higher',
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        for name in SPEED_LIST:
            speed, is_new = (NetworkSpeed.objects
                             .get_or_create(name=name))
            if is_new:
                print u"Imported speed: %s" % speed
        print "Done!"
