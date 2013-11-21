import urlparse

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):

    def handle(self, *args, **options):
        parsed_url = urlparse.urlparse(settings.SITE_URL)
        Site.objects.all().update(domain=parsed_url.netloc,
                                  name=parsed_url.netloc)
        print "Done!"
