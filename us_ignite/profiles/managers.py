from django.db import models

from django.conf import settings


class ProfileActiveManager(models.Manager):
    """Returns the profiles that have been activated.

    Avoids listing any super user.
    """

    def get_query_set(self):
        kwargs = {'user__is_active': True}
        if not settings.DEBUG:
            kwargs['user__is_superuser'] = False
        return (super(ProfileActiveManager, self).get_query_set().
                select_related('user')
                .filter(**kwargs))
