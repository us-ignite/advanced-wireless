from datetime import timedelta
from random import choice

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from us_ignite.apps.models import (
    Application, Domain, Feature, Page, PageApplication)
from us_ignite.challenges.models import Challenge, Entry, Question
from us_ignite.dummy import text, images
from us_ignite.events.models import Event
from us_ignite.resources.models import Resource
from us_ignite.hubs.models import Hub, HubMembership
from us_ignite.organizations.models import Organization, OrganizationMember
from us_ignite.profiles.models import Profile


class Command(BaseCommand):

    domain_list = Domain.objects.all()
    feature_list = Feature.objects.all()

    def _create_users(self):
        users = ['banana', 'apple', 'orange', 'peach']
        for f in users:
            user, is_new = User.objects.get_or_create(username=f, is_active=True)
            if is_new and choice([True, False]):
                bio = text.random_paragraphs(2)
                Profile.objects.create(user=user, name=f, bio=bio)
        return True

    def _get_user(self):
        return User.objects.all().order_by('?')[0]

    def _get_domain(self):
        return choice(self.domain_list)

    def _get_feature(self):
        return choice(self.feature_list)

    def _choice(self, *args):
        """Choice between the args and an empty string."""
        return choice([''] + list(args))

    def _get_url(self):
        return 'http://us-ignite.org'

    def _create_app(self):
        data = {
            'name': text.random_words(3),
            'stage': choice(Application.STAGE_CHOICES)[0],
            'status': choice(Application.STATUS_CHOICES)[0],
            'website': self._get_url(),
            'summary': self._choice(text.random_words(20))[:140],
            'impact_statement': text.random_words(20)[:140],
            'description': text.random_paragraphs(4),
            'roadmap': self._choice(text.random_words(30)),
            'assistance': self._choice(text.random_words(30)),
            'team_description': self._choice(text.random_words(30)),
            'acknowledgments': self._choice(text.random_words(30)),
            'domain': self._get_domain(),
            'is_featured': choice([True, False]),
            'owner': self._get_user(),
            'image': images.random_image(u'%s.png' % text.random_words(1)),
        }
        return Application.objects.create(**data)

    def _create_page(self):
        data = {
            'name': text.random_words(3),
            'status': choice(Application.STATUS_CHOICES)[0],
            'description': text.random_paragraphs(2),
        }
        page = Page.objects.create(**data)
        app_list = (Application.objects
                    .filter(status=Application.PUBLISHED).order_by('?')[:10])
        for i, app in enumerate(app_list):
            PageApplication.objects.create(page=page, application=app, order=i)

    def _get_start_date(self):
        days = choice(range(-5, 50))
        return timezone.now() + timedelta(days=days)

    def _create_hub(self):
        data = {
            'name': text.random_words(3),
            'guardian': choice([None, self._get_user()]),
            'summary': text.random_words(10),
            'description': text.random_paragraphs(3),
            'image': images.random_image(u'%s.png' % text.random_words(1)),
            'website': self._get_url(),
            'status': choice(Hub.STATUS_CHOICES)[0],
            'is_featured': choice([True, False]),
        }
        hub = Hub.objects.create(**data)
        self._create_hub_membership(hub)
        return hub

    def _create_hub_membership(self, hub):
        for user in User.objects.all().order_by('?')[:3]:
            data = {
                'hub': hub,
                'user': user,
            }
            HubMembership.objects.create(**data)

    def _get_hub(self):
        return Hub.objects.filter(status=Hub.PUBLISHED).order_by('?')[0]

    def _create_event(self):
        start_date = self._get_start_date()
        end_date = start_date + timedelta(hours=5)
        data = {
            'name': text.random_words(5),
            'status': choice(Event.STATUS_CHOICES)[0],
            'image': images.random_image(u'%s.png' % text.random_words(1)),
            'start_datetime': start_date,
            'end_datetime': choice([None, end_date]),
            'venue': text.random_words(7),
            'description': text.random_paragraphs(2),
            'is_featured': choice([True, False]),
            'user': self._get_user(),
        }
        event = Event.objects.create(**data)
        for i in range(0, 3):
            event.hubs.add(self._get_hub())
        return event

    def _create_challenge(self):
        start_date = self._get_start_date()
        end_date = start_date + timedelta(days=15)
        data = {
            'name': text.random_words(5),
            'status': choice(Challenge.STATUS_CHOICES)[0],
            'start_datetime': start_date,
            'end_datetime': end_date,
            'url': self._get_url(),
            'is_external': choice([True, False]),
            'summary': text.random_paragraphs(1),
            'description': text.random_paragraphs(3),
            'image': images.random_image(u'%s.png' % text.random_words(1)),
            'user': self._get_user(),
        }
        challenge = Challenge.objects.create(**data)
        for i in range(0, 10):
            self._create_question(challenge, i)
        return challenge

    def _create_question(self, challenge, order=0):
        data = {
            'challenge': challenge,
            'question': u'%s?' % text.random_words(7),
            'is_required': choice([True, False]),
            'order': order,
        }
        return Question.objects.create(**data)

    def _create_entries(self):
        apps = Application.objects.all().order_by('?')
        for challenge in Challenge.objects.all():
            for i in range(0, choice(range(1, 10))):
                data = {
                    'challenge': challenge,
                    'application': apps.pop(),
                    'status': choice(Entry.STATUS_CHOICES)[0],
                    'notes': self._choice(text.random_words(10)),
                }
                Entry.objects.create(**data)
        return True

    def _create_organization(self):
        name = text.random_words(3)
        data = {
            'name': name,
            'slug': slugify(name),
            'status': choice(Organization.STATUS_CHOICES)[0],
            'bio': self._choice(text.random_words(30)),
            'image': images.random_image(u'%s.png' % text.random_words(1)),
        }
        organization = Organization.objects.create(**data)
        self._create_organization_membership(organization)
        return organization

    def _create_organization_membership(self, organization):
        for user in User.objects.all().order_by('?')[:3]:
            data = {
                'organization': organization,
                'user': user,
            }
            OrganizationMember.objects.create(**data)

    def _create_resource(self):
        name = text.random_words(4)
        data = {
            'name': name,
            'slug': slugify(name),
            'status': choice(Resource.STATUS_CHOICES)[0],
            'description': text.random_paragraphs(1),
            'contact': self._get_user(),
            'author': choice([self._get_user(), None]),
            'url': self._get_url(),
            'is_featured': choice([True, False]),
        }
        return Resource.objects.create(**data)

    def handle(self, *args, **options):
        message = ('This command will IRREVERSIBLE poison the existing '
                   'database by adding dummy content and images. '
                   'Proceed? [y/N] ')
        response = raw_input(message)
        if not response or not response == 'y':
            print 'Phew, aborted!'
            exit(0)
        call_command('app_load_fixtures')
        call_command('awards_load_fixtures')
        call_command('common_load_fixtures')
        call_command('snippets_load_fixtures')
        call_command('events_load_fixtures')
        call_command('resources_load_fixtures')
        call_command('blog_import')
        print u'Adding users'
        self._create_users()
        print u'Adding organizations'
        for i in range(1, 5):
            self._create_organization()
        print u'Generating applications.'
        for i in range(1, 30):
            self._create_app()
        print u'Generating app pages.'
        for i in range(1, 5):
            self._create_page()
        print u'Generating hubs.'
        for i in range(1, 10):
            self._create_hub()
        print u'Generate events.'
        for i in range(1, 10):
            self._create_event()
        print u'Generate challenges.'
        for i in range(1, 10):
            self._create_challenge()
        print u'Generate resources.'
        for i in range(1, 10):
            self._create_resource()
        call_command('blog_import')
