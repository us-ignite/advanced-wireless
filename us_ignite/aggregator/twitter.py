import logging
import twython

from django.conf import settings


logger = logging.getLogger('us_ignite.aggregator.twitter')


def get_setting(name):
    return getattr(settings, name, None)


def _get_access_token(key, secret):
    twitter = twython.Twython(key, secret, oauth_version=2)
    return twitter.obtain_access_token()


def get_timeline(username, total=5):
    """Returns the latest tweets from a given ``User``."""
    TWITTER_KEY = get_setting('TWITTER_API_KEY')
    TWITTER_SECRET = get_setting('TWITTER_API_SECRET')
    # Bail out if the key and secret are not pressent
    if not all([TWITTER_KEY, TWITTER_SECRET]):
        return []
    token = _get_access_token(TWITTER_KEY, TWITTER_SECRET)
    twitter = twython.Twython(TWITTER_KEY, access_token=token)
    try:
        timeline = twitter.get_user_timeline(screen_name=username, count=total)
    except Exception, e:
        logger.exception(e)
        return []
    return timeline[:total]
