from datetime import timedelta
from random import choice

from django.contrib.auth.models import User
from django.core.management import call_command
from django.core.management.base import BaseCommand
from django.utils import timezone
from django.utils.text import slugify

from us_ignite.apps.models import (
    Application,
    Domain,
    Page,
    PageApplication,
)
from us_ignite.blog.models import Post
from us_ignite.challenges.models import Challenge, Entry, Question
from us_ignite.dummy import text, images, locations
from us_ignite.events.models import Event
from us_ignite.resources.models import Resource
from us_ignite.hubs.models import Hub, HubMembership
from us_ignite.organizations.models import Organization, OrganizationMember
from us_ignite.profiles.models import Profile


def _choice(*args):
    """Choice between the args and an empty string."""
    return choice([''] + list(args))


def _get_start_date():
    days = choice(range(-5, 50))
    return timezone.now() + timedelta(days=days)


def _create_users():
    users = ['banana', 'apple', 'orange', 'cherry', 'lemon', 'grape']
    profile_list = []
    for f in users:
        email =  '%s@us-ignite.org' % f
        user, is_new = User.objects.get_or_create(
            username=f, is_active=True, email=email)
        if is_new and choice([True, False]):
            data = {
                'bio': text.random_paragraphs(2),
                'position': locations.get_location(),
                'user': user,
                'name': f,
            }
            profile = Profile.objects.create(**data)
            profile_list.append(profile)
    return profile_list


def _get_user():
    return User.objects.all().order_by('?')[0]


def _get_url():
    return u'http://us-ignite.org'


def _get_domain():
    return Domain.objects.all().order_by('?')[0]


def _get_hub():
    return Hub.objects.filter(status=Hub.PUBLISHED).order_by('?')[0]


def _create_organization_membership(organization):
    for user in User.objects.all().order_by('?')[:3]:
        data = {
            'organization': organization,
            'user': user,
        }
        OrganizationMember.objects.create(**data)


def _create_organization():
    name = text.random_words(3)
    data = {
        'name': name.title(),
        'slug': slugify(name),
        'status': choice(Organization.STATUS_CHOICES)[0],
        'bio': _choice(text.random_words(30)),
        'image': images.random_image(u'%s.png' % text.random_words(1)),
        'position': locations.get_location(),
    }
    organization = Organization.objects.create(**data)
    _create_organization_membership(organization)
    return organization


def _create_app():
    data = {
        'name': text.random_words(3).title(),
        'stage': choice(Application.STAGE_CHOICES)[0],
        'status': choice(Application.STATUS_CHOICES)[0],
        'website': _get_url(),
        'summary': _choice(text.random_words(20))[:140],
        'impact_statement': text.random_words(20)[:140],
        'description': text.random_paragraphs(4),
        'roadmap': _choice(text.random_words(30)),
        'assistance': _choice(text.random_words(30)),
        'team_description': _choice(text.random_words(30)),
        'acknowledgments': _choice(text.random_words(30)),
        'domain': _get_domain(),
        'is_featured': choice([True, False]),
        'owner': _get_user(),
        'image': images.random_image(u'%s.png' % text.random_words(1)),
    }
    return Application.objects.create(**data)


def _create_page():
    data = {
        'name': text.random_words(3).title(),
        'status': choice(Application.STATUS_CHOICES)[0],
        'description': text.random_paragraphs(2),
    }
    page = Page.objects.create(**data)
    app_list = (Application.objects
                .filter(status=Application.PUBLISHED).order_by('?')[:10])
    for i, app in enumerate(app_list):
        PageApplication.objects.create(page=page, application=app, order=i)


def _create_hub_membership(hub):
    for user in User.objects.all().order_by('?')[:3]:
        data = {
            'hub': hub,
            'user': user,
        }
        HubMembership.objects.create(**data)


def _create_hub():
    data = {
        'name': text.random_words(3).title(),
        'contact': choice([None, _get_user()]),
        'summary': text.random_words(10),
        'description': text.random_paragraphs(3),
        'image': images.random_image(u'%s.png' % text.random_words(1)),
        'website': _get_url(),
        'status': choice(Hub.STATUS_CHOICES)[0],
        'is_featured': choice([True, False]),
    }
    hub = Hub.objects.create(**data)
    _create_hub_membership(hub)
    return hub


def _create_event():
    start_date = _get_start_date()
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
        'user': _get_user(),
        'position': locations.get_location(),
    }
    event = Event.objects.create(**data)
    for i in range(0, 3):
        event.hubs.add(_get_hub())
    return event


def _create_challenge():
    start_date = _get_start_date()
    end_date = start_date + timedelta(days=15)
    data = {
        'name': text.random_words(5).title(),
        'status': choice(Challenge.STATUS_CHOICES)[0],
        'start_datetime': start_date,
        'end_datetime': end_date,
        'url': _get_url(),
        'is_external': choice([True, False]),
        'summary': text.random_paragraphs(1),
        'description': text.random_paragraphs(3),
        'image': images.random_image(u'%s.png' % text.random_words(1)),
        'user': _get_user(),
    }
    challenge = Challenge.objects.create(**data)
    for i in range(0, 10):
        _create_question(challenge, i)
    _create_entries(challenge)
    return challenge


def _create_question(challenge, order=0):
    data = {
        'challenge': challenge,
        'question': u'%s?' % text.random_words(7),
        'is_required': choice([True, False]),
        'order': order,
    }
    return Question.objects.create(**data)


def _create_entries(challenge):
    apps = list(Application.objects.all().order_by('?'))
    entry_list = []
    for i in range(0, choice(range(1, 10))):
        data = {
            'challenge': challenge,
            'application': apps.pop(),
            'status': choice(Entry.STATUS_CHOICES)[0],
            'notes': _choice(text.random_words(10)),
        }
        entry = Entry.objects.create(**data)
        entry_list.append(entry)
    return entry_list


def _create_resource():
    name = text.random_words(4)
    data = {
        'name': name.title(),
        'slug': slugify(name),
        'status': choice(Resource.STATUS_CHOICES)[0],
        'description': text.random_paragraphs(1),
        'contact': _get_user(),
        'author': choice([_get_user(), None]),
        'url': _get_url(),
        'is_featured': choice([True, False]),
        'image': images.random_image(u'%s.png' % text.random_words(1)),
    }
    return Resource.objects.create(**data)

def _feature_posts():
    for post in Post.objects.all().order_by('?')[:5]:
        post.is_featured = True
        post.save()


def _load_fixtures():
    """Loads initial fixtures"""
    call_command('app_load_fixtures')
    call_command('awards_load_fixtures')
    call_command('common_load_fixtures')
    call_command('snippets_load_fixtures')
    call_command('events_load_fixtures')
    call_command('resources_load_fixtures')
    call_command('hubs_load_fixtures')
    call_command('blog_import')


class Command(BaseCommand):

    def handle(self, *args, **options):
        message = ('This command will IRREVERSIBLE poison the existing '
                   'database by adding dummy content and images. '
                   'Proceed? [y/N] ')
        response = raw_input(message)
        if not response or not response == 'y':
            print 'Phew, aborted!'
            exit(0)
        print u'Loading initial fixtures.'
        _load_fixtures()
        print u'Featuring Posts'
        _feature_posts()
        print u'Adding users.'
        _create_users()
        print u'Adding organizations.'
        for i in range(5, 10):
            _create_organization()
        print u'Adding applications.'
        for i in range(20, 40):
            _create_app()
        print u'Adding app pages.'
        for i in range(5, 10):
            _create_page()
        print u'Adding hubs.'
        for i in range(10, 20):
            _create_hub()
        print u'Adding events.'
        for i in range(15, 30):
            _create_event()
        print u'Adding challenges.'
        for i in range(15, 30):
            _create_challenge()
        print u'Adding resources.'
        for i in range(15, 30):
            _create_resource()
        print u'Done.'
