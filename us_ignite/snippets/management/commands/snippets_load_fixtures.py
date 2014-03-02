from django.core.management.base import BaseCommand

from us_ignite.snippets.models import Snippet


FIXTURES = [
    {
        'slug': 'home-box',
        'name': 'UP NEXT: LOREM IPSUM',
        'body': '',
        'url_text': 'GET INVOLVED',
        'url': '',
    },
    {
        'slug': 'featured',
        'name': 'FEATURED CONTENT',
        'body': '',
        'url_text': 'FEATURED',
        'url': '',
    },
    {
        'slug': 'welcome-email',
        'name': 'Welcome to US Ignite',
        'body': '',
        'url_text': '',
        'url': '',
    },
]


class Command(BaseCommand):

    def handle(self, *args, **options):
        for data in FIXTURES:
            try:
                # Ignore existing snippets:
                Snippet.objects.get(slug=data['slug'])
                continue
            except Snippet.DoesNotExist:
                pass
            data.update({
                'status': Snippet.PUBLISHED,
            })
            Snippet.objects.create(**data)
            print u'Importing %s' % data['slug']
        print "Done!"
