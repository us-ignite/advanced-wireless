import logging
import pytz
import requests

from StringIO import StringIO

from django.contrib.auth.models import User
from django.core import files
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.utils import timezone
from django.utils.dateparse import parse_datetime

from us_ignite.apps.models import Application, ApplicationURL, Domain
from us_ignite.profiles.models import Profile


logger = logging.getLogger('us_ignite.apps.importer')

TIMEZONE = 'America/New_York'


def parse_date(date_str):
    naive = parse_datetime(date_str)
    return pytz.timezone(TIMEZONE).localize(naive, is_dst=None)


def import_author(data):
    email = data['email']
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        user = User.objects.create_user(
            data['username'], email, first_name=data['name'][:30])
    profile, is_new = Profile.objects.get_or_create(user=user)
    if is_new:
        profile.website = data['website']
        profile.save()
    return user


def get_domain(data):
    categories = {
        'education': 'education-workforce',
        'advanced-manufacturing': 'advanced-manufacturing',
        'health-it': 'healthcare',
        'public-safety': 'public-safety',
        'clean-energy': 'energy',
    }
    old_slug = data['slug']
    if old_slug in categories:
        return Domain.objects.get(slug=categories[old_slug])
    assert False, data


def get_stage(data):
    name = data['name'].lower()
    stages = {
        'development': Application.ALPHA,
        'ideation': Application.IDEA,
    }
    if name in stages:
        return stages[name]
    assert False, name


def import_urls(application, blog, repo):
    if blog:
        blog_url, is_new  = (ApplicationURL.objects
                             .get_or_create(application=application, url=blog))
        blog_url.name = 'Blog'
        blog_url.save()
    else:
        blog_url = None
    if repo:
        repo_url, is_new = (ApplicationURL.objects
                            .get_or_create(application=application, url=repo))
        repo_url.name = 'Repository'
        repo_url.save()
    else:
        repo_url = None
    return (blog_url, repo_url)


def import_image(path, key):
    url = 'https://mozillaignite.org%s' % path
    if default_storage.exists(key):
        logger.debug('Ignoring existing file: %s', key)
        return key
    logger.debug('Downloading: %s',  url)
    response = requests.get(url, verify=False)
    image_file = files.File(StringIO(response.content))
    return default_storage.save(key, ContentFile(image_file.read()))


def _get_key_from_url(url, prefix='apps'):
    suffix = url.split('/')[-1]
    return u'%s/%s' % (prefix, suffix)


_title = lambda t: u'\n###%s\n' % t


def import_app(data):
    author_data = data.get('created_by')
    author = import_author(author_data) if author_data else None
    slug = 'MI-%s' % data['slug']
    application, is_new = Application.objects.get_or_create(slug=slug)
    application.name = data['name']
    application.summary = data['brief_description']
    application.team_description = data['collaborators']
    application.impact_statement = data['life_improvements']
    application.domain = get_domain(data['category'])
    application.owner = author
    application.stage = get_stage(data['phase'])
    application.website = data['blog_url'] or data['repository_url']
    application.created = parse_date(data['created_on'])
    application.modified = parse_date(data['updated_on'])
    if data['is_draft']:
        application.status = Application.DRAFT
    else:
        application.status = Application.PUBLISHED
    description_list = [
        data['description'],
    ]
    if data['take_advantage']:
        description_list += [
            _title('How does your idea take advantage of '
                   'next-generation networks?'),
            data['take_advantage']]
    if data['required_effort']:
        description_list += [
            _title('How much effort do you expect this work to take?'),
            data['required_effort']]
    if data['interest_making']:
        description_list += [_title('Interest making'), data['interest_making']]
    application.description = '\n'.join(description_list)
    application.notes = ('Imported from the Mozilla Ignite site '
                         '(%s).' % timezone.now())
    image_url = data.get('sketh_note')
    if image_url:
        application.image = import_image(
            image_url, _get_key_from_url(image_url))
    application.save()
    application.tags.add('mozillaignite')
    import_urls(application, data['blog_url'], data['repository_url'])
    return application


def digest_payload(payload):
    imported_apps = []
    for app in payload:
        imported_apps.append(import_app(app))
    return [a for a in imported_apps if a]
