import requests

from django.core.management.base import BaseCommand, CommandError

from us_ignite.actionclusters import importer


class Command(BaseCommand):
    help = 'Import the given JSON file.'

    def handle(self, url, *args, **options):
        response = requests.get(url)
        if not response.status_code == 200:
            raise CommandError('Issue getting the file %s', response.content)
        result = importer.digest_payload(response.json())
        print u'%s action clusters have been imported.' % len(result)
        print u'Done!'
