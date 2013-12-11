import hashlib

from urlparse import urlparse

from django.core.cache import cache
from django.template.loader import render_to_string

from us_ignite.aggregator import github, twitter


def render_github(parsed_url):
    path_bits = parsed_url.path.split('/')
    try:
        username = path_bits.pop(1)
    except IndexError:
        return u''
    try:
        project = path_bits.pop(1)
    except IndexError:
        project = None
    # Latest commits:
    commit_list = github.get_commits(username, project) if project else []
    context = {
        'parsed_url': parsed_url,
        'username': username,
        'project': project,
        'commit_list': commit_list,
    }
    return render_to_string('apps/includes/github.html', context)


def render_twitter(parsed_url):
    path_bits = parsed_url.path.split('/')
    try:
        username = path_bits.pop(1)
    except IndexError:
        return u''
    tweet_list = twitter.get_timeline(username)
    context = {
        'parsed_url': parsed_url,
        'username': username,
        'tweet_list': tweet_list,
    }
    return render_to_string('apps/includes/twitter.html', context)


SUPPORTED_URLS = {
    'github.com': render_github,
    'twitter.com': render_twitter,
}


def render_url(url):
    parsed_url = urlparse(url)
    renderer = SUPPORTED_URLS.get(parsed_url.netloc)
    return renderer(parsed_url) if renderer else None


def _get_cache_key(url, prefix=''):
    suffix = hashlib.md5(url).hexdigest()
    return '%s%s' % (prefix, suffix)


def cached_render_url(url):
    cache_key = _get_cache_key(url, prefix='RENDERER')
    response = cache.get(cache_key)
    if response:
        return response
    rendered = render_url(url)
    # Cache for 10 minutes:
    cache.set(cache_key, rendered, 60 * 10)
    return rendered
