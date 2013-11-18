import logging
import requests

logger = logging.getLogger('us_ignite.aggregator.github')


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
        return response.json()[:total]
    except ValueError:
        return []
