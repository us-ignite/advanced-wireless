from django.contrib.auth.models import User, AnonymousUser
from django.core.urlresolvers import reverse
from django.contrib.messages.storage.base import BaseStorage, Message

from django.test import client

from mock import Mock


def get_login_url(url):
    """Returns an expected login URL."""
    return ('%s?next=%s' % (reverse('auth_login'), url))


def get_anon_mock():
    """Generate an anon user mock."""
    return AnonymousUser()


def get_user_mock():
    """Generate an authed user mock."""
    user = Mock(spec=User)
    user.is_authenticated.return_value = True
    return user


def get_request(method, *args, **kwargs):
    """Generatse a request with the given ``method``."""
    user = kwargs.pop('user', None)
    factory = client.RequestFactory()
    method_action = getattr(factory, method)
    request = method_action(*args, **kwargs)
    if user:
        request.user = user
    return request


def get_management_form(prefix, initial=0, total=0, max_num=3):
    default = {
        '%sTOTAL_FORMS' % prefix: total,
        '%sINITIAL_FORMS' % prefix: initial,
        '%sMAX_NUM_FORMS' % prefix: max_num,
    }
    return default


def get_inline_payload(
        formset_class, instance=None, data_list=None, max_num=3, **kwargs):
    formset = formset_class(instance=instance)
    data_list = data_list if data_list else []
    prefix = '%s_set-' % formset.model.__name__.lower()
    default = get_management_form(prefix, len(data_list), max_num)
    _inline_tuple = lambda i, k, v: ('%s%s-%s' % (prefix, i, k), v)
    instance_name = formset.instance.__class__.__name__.lower()
    pk = '' if not instance else instance.pk
    for i, inline in enumerate(data_list):
        inline_default = {
            '%s%s-DELETE' % (prefix, i): '',
            '%s%s-%s' % (prefix, i, instance_name): pk,
        }
        inline_item = dict(_inline_tuple(i, k, v) for k, v in inline.items())
        inline_default.update(inline_item)
        default.update(inline_default)
    default.update(kwargs)
    return default


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
