import logging

from django.db import models


logger = logging.getLogger('us_ignite.profiles')


class ProfileActiveManager(models.Manager):
    """Returns the profiles that have been activated.

    Avoids listing any super user.
    """

    def get_query_set(self):
        kwargs = {'user__is_active': True}
        return (super(ProfileActiveManager, self).get_query_set().
                select_related('user')
                .filter(**kwargs))

    def get_or_create_for_user(self, user, **kwargs):
        profile, is_new = self.get_or_create(user=user)
        logger.debug('Creating profile for: %s' , user)
        return profile
