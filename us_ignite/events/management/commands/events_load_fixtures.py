from django.core.management.base import BaseCommand

from us_ignite.events.models import Audience


AUDIENCE_LIST = (
    ('Developer', 'developer'),
    ('End-User', 'end-user'),
    ('Community Member', 'community-member'),
    ('Community Leader', 'community-leader'),
    ('Government', 'government'),
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        for name, slug in AUDIENCE_LIST:
            audience, is_new = (Audience.objects
                                .get_or_create(name=name, slug=slug))
            if is_new:
                print u"Imported audience: %s" % audience
        print "Done!"
