from django.core.urlresolvers import reverse


def get_login_url(url):
    """Returns an expected login URL."""
    return '%s?next=%s' % (reverse('auth_login'), url)
