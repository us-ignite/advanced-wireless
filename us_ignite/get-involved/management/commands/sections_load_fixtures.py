from django.core.management.base import BaseCommand
from django.conf import settings

from us_ignite.common import files
from us_ignite.sections.models import Sponsor


SPONSOR_LIST = (
    ('Ciena', 'ciena.png'),
    ('HP', 'hp.png'),
    ('Mozilla', 'mozilla.png'),
    ('NEC', 'nec.png'),
    ('Internet 2', 'internet2.png'),
    ('Verizon', 'verizon.png'),
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        sponsor_list = []
        for i, (name, image_name) in enumerate(SPONSOR_LIST):
            sponsor, is_new = Sponsor.objects.get_or_create(name=name)
            if not is_new:
                continue
            sponsor.order = i
            file_key = 'sponsor/%s' % image_name
            url = '%simg/logos/%s' % (settings.STATIC_URL, image_name)
            if not url.startswith('http'):
                url = 'http://localhost%s' % url
            sponsor.image = files.import_file(url, file_key)
            sponsor.save()
            sponsor_list.append(sponsor)
        print u'Imported %s sponsors' % len(sponsor_list)
