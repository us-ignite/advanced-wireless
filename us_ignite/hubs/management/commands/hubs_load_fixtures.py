from django.core.management.base import BaseCommand

from us_ignite.hubs.models import NetworkSpeed


SPEED_LIST = (
    ('100 Mbps symmetric or higher', '100-mbps-symmetric'),
    ('200 Mbps symmetric or higher', '200-mbps-symmetric'),
    ('1 Gbps symmetric or higher', '1-gbps-symmetric'),
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        for name, slug in SPEED_LIST:
            speed, is_new = (NetworkSpeed.objects
                             .get_or_create(name=name, slug=slug))
            if is_new:
                print u"Imported speed: %s" % speed
        print "Done!"
