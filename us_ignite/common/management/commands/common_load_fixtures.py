import urlparse

from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site

from us_ignite.profiles.models import Category, Interest


INTEREST_LIST = (
    ('SDN', 'sdn'),
    ('OpenFlow', 'openflow'),
    ('Ultra fast', 'ultra-fast'),
    ('Advanced wireless', 'advanced-wireless'),
    ('Low-latency', 'low-latency'),
    ('Local cloud/edge computing', 'local-cloud-edge-computing'),
    ('Healthcare', 'healthcare'),
    ('Education & Workforce development', 'education-workforce-development'),
    ('Energy', 'energy'),
    ('Transportation', 'transportation'),
    ('Advanced Manufacturing', 'advanced-manufacturing'),
    ('Public Safety', 'public-safety'),
)


CATEGORY_LIST = [
    'Developer',
    'Community leader',
    'Subject matter expert',
    'Designer',
    'Project manager',
    'Network engineer',
    'Funder',
    'Press/media',
    'Interested party',
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        parsed_url = urlparse.urlparse(settings.SITE_URL)
        Site.objects.all().update(domain=parsed_url.netloc,
                                  name=parsed_url.netloc)
        print u'Updated site URL.'
        for name, slug in INTEREST_LIST:
            interest, is_new = (Interest.objects
                                .get_or_create(name=name, slug=slug))
            if is_new:
                print u'Imported interest: %s.' % interest
        for name in CATEGORY_LIST:
            category, is_new = Category.objects.get_or_create(name=name)
            if is_new:
                print u'Imported category: %s.' % category
