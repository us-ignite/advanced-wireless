import logging
import requests

from django.utils.html import strip_tags

logger = logging.getLogger('us_ignite.aggregator.github')


def clean_commit(commit):
    """Returns the first line of the commit."""
    commit = strip_tags(commit)
    # Lines with meaningful values:
    lines = [line for line in commit.splitlines() if line.strip()]
    return lines[0] if lines else u'Missing commit message.'


def get_commits(user, project, total=5):
    """Returns the latest commits of the project"""
    url = ('https://api.github.com/repos/%s/%s/commits' % (user, project))
    try:
        response = requests.get(url)
    except Exception, e:
        logger.exception(e)
        return []
    if not response.status_code == 200:
        logger.info('Failed to grab commits from %s. Received: %s',
                    url, response.content)
        return []
    try:
        response = response.json()[:total]
    except ValueError:
        return []
    for item in response:
        item['cleaned_commit'] = clean_commit(item['commit']['message'])
    return response
