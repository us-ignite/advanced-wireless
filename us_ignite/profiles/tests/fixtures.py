from django.contrib.auth.models import User

from us_ignite.profiles.models import Profile


def get_user(slug, password=None, is_superuser=False, is_staff=False, **kwargs):
    defaults = {
        'username': slug,
        'email': '%s@%s.org' % (slug, slug),
        'first_name': slug,
    }
    defaults.update(kwargs)
    user, is_new = User.objects.get_or_create(**defaults)
    password = password if password else slug
    user.set_password(password)
    user.is_superuser = is_superuser
    user.is_staff = is_staff
    user.save()
    return user


def get_profile(**kwargs):
    defaults = {}
    if 'name' in kwargs:
        name = kwargs.pop('name')
    if not 'user' in kwargs:
        defaults['user'] = get_user('john', first_name=name)
    defaults.update(kwargs)
    profile, is_new = Profile.objects.get_or_create(**defaults)
    return profile
