from django.db import models


class ProfileActiveManager(models.Manager):
    """Returns the profiles that have been activated.

    Avoids listing any super user.
    """

    def get_query_set(self):
        return (super(ProfileActiveManager, self).get_query_set().
                select_related('user')
                .filter(user__is_active=True, user__is_superuser=False))
