from django.core.management.base import BaseCommand
from django.template.loader import render_to_string

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
        'body': render_to_string('profile/emails/welcome.html'),
        'url_text': '',
        'url': '',
    },
    {
        'slug': 'blog-sidebar',
        'name': 'Blog sidebar featured content.',
        'body': '',
        'url_text': '',
        'url': '',
    },
    {
        'slug': 'profile-welcome',
        'name': 'Welcome message in the profile',
        'body': 'Lorem ipsum',
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
