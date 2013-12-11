from django.db import models


class ProfileActiveManager(models.Manager):
    """Returns the profiles that have been activated.

    Avoids listing any super user.
    """

    def get_query_set(self):
        kwargs = {'user__is_active': True}
        return (super(ProfileActiveManager, self).get_query_set().
                select_related('user')
                .filter(**kwargs))
