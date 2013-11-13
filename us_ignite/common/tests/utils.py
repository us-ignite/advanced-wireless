from django.core.urlresolvers import reverse
from django.contrib.messages.storage.base import BaseStorage, Message


def get_login_url(url):
    """Returns an expected login URL."""
    return ('%s?next=%s' % (reverse('auth_login'), url))


class TestMessagesBackend(BaseStorage):
    """
    When unit testing a django view the ``messages`` middleware
    will be missing. This backend will provision a simple
    messaging midleware.

    Usage::

    from django.test import client
    from us_ignite.common.tests import utils

    factory = client.RequestFactory()
    request = factory.get('/')
    request._messages = utils.TestMessagesBackend(request)
    """
    def __init__(self, request, *args, **kwargs):
        self._loaded_data = []
        super(TestMessagesBackend, self).__init__(request, *args, **kwargs)

    def add(self, level, message, extra_tags=''):
        self._loaded_data.append(
            Message(level, message, extra_tags=extra_tags))
