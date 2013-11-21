from django.core.management.base import BaseCommand

from us_ignite.awards.models import Award


AWARD_LIST = (
    'Gold Star',
    'Gigabit Community Fund',
    'Mozilla Ignite team',
    'NSF Ignite Award',
)


class Command(BaseCommand):

    def handle(self, *args, **options):
        for award_name in AWARD_LIST:
            award, is_new = Award.objects.get_or_create(name=award_name)
            if is_new:
                print "Imported award: %s" % award_name
        print "Done!"
