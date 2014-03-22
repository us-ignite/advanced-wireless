from django.core.management.base import BaseCommand

from us_ignite.events.models import Audience, EventType


AUDIENCE_LIST = (
    ('Developer', 'developer'),
    ('End-User', 'end-user'),
    ('Community Member', 'community-member'),
    ('Community Leader', 'community-leader'),
    ('Government', 'government'),
)

TYPE_LIST = (
    ('Workshop', 'workshop'),
    ('Conference', 'conference'),
    ('Meeting', 'meeting'),
    ('Networking', 'networking'),
    ('Challenge', 'challenge'),
    ('Hackaton', 'hackaton'),
    ('Other', 'other'),
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        for name, slug in AUDIENCE_LIST:
            audience, is_new = (Audience.objects
                                .get_or_create(name=name, slug=slug))
            if is_new:
                print u"Imported audience: %s" % audience
        for name, slug in TYPE_LIST:
            event_type, is_new = (EventType.objects
                                  .get_or_create(name=name, slug=slug))
            if is_new:
                print u"Imported event type: %s" % event_type
