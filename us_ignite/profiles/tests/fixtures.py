from django.contrib.auth.models import User

from us_ignite.profiles.models import Profile


def get_user(slug, **kwargs):
    defaults = {
        'username': slug,
        'password': slug,
        'email': '%s@%s.org' % (slug, slug),
        'first_name': slug,
    }
    defaults.update(kwargs)
    return User.objects.create_user(**defaults)


def get_profile(**kwargs):
    defaults = {}
    if not 'user' in kwargs:
        defaults['user'] = get_user('john')
    defaults.update(kwargs)
    return Profile.objects.create(**defaults)
