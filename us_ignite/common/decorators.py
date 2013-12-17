import hashlib
import functools

from django.contrib.auth.views import redirect_to_login
from django.core.cache import cache
from django.http import HttpResponseRedirect, HttpResponse
from django.template.response import TemplateResponse


def group_required(group_list):
    """Restricts access to a ``view`` by ``Group`` membership.

    When the user is not logged in is redirected to the
    authentication page.
    If the user is logged but is not member of the group
    is shown an unavailable page.

    The ``group_list`` argument can be a list of groups
    or a single group. Usage::

        # Single group
        @group_required('custom-group')
        def view(request)
            ...

        # Multi-group
        @group_required(['group-a', 'group-b'])
        def view(request)
            ...
    """
    def decorator(function):
        @functools.wraps(function)
        def wrapper(request, *args, **kwargs):
            # Transform the string in a list for querying:
            if isinstance(group_list, basestring):
                name_list = [group_list]
            else:
                name_list = group_list
            if not isinstance(name_list, list):
                raise ValueError('``group_list`` must be a ``Group`` list.')
            if request.user and request.user.is_authenticated():
                # Make sure the user is in this in any of these groups
                if request.user.groups.filter(name__in=name_list).count():
                    return function(request, *args, **kwargs)
                else:
                    # User does not belong to this group
                    # show unavailable page:
                    return TemplateResponse(request, 'unavailable.html', {})
            else:
                # User must be logged in to access this area:
                path = request.build_absolute_uri()
                return redirect_to_login(path)
        return wrapper
    return decorator


def not_auth_required(function):
    """Redirects the user to the homepage when the user is logged in."""
    @functools.wraps(function)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated():
            return function(request, *args, **kwargs)
        return HttpResponseRedirect('/')
    return wrapper


def get_request_key(request):
    """Determines the most suitable key to be used to throttle from a request.

    - Authenticated user ID.
    - ``HTTP_X_FORWARDED_FOR`` header.
    - ``X_FORWARDED_FOR`` header.
    - ``REMOTE_ADDR`` header.
    """
    if request.user.is_authenticated():
        prefix = 'user.%s' % request.user.pk
    else:
        prefix = (request.META.get('HTTP_X_FORWARDED_FOR')
                  or request.META.get('X_FORWARDED_FOR')
                  or request.META.get('REMOTE_ADDR')
                  or 'NO-ADDR')
    return hashlib.md5('%s.%s' % (prefix, request.path_info)).hexdigest()


def throttle_view(methods=None, duration=15, prefix=''):
    """Decorator that throttles the specified methods ``POST`` and ``GET``
    by default, uses as value:

    - Authenticated user ID.
    - ``HTTP_X_FORWARDED_FOR`` header.
    - ``X_FORWARDED_FOR`` header.
    - Or ``REMOTE_ADDR`` header

    Also accepts a prefix for cache invalidation.

    Usage:

    - Throotle with the ``POST`` method by 30 seconds

    @throttle_view(methods=['POST'], duration=30, prefix='FOO')

    - Throotle with the default values

    @throotle_view()
    """
    def decorator(function):
        @functools.wraps(function)
        def inner(request, *args, **kwargs):
            throttled_methods = methods if methods else ['POST', 'GET']
            if request.method in throttled_methods:
                key = '%s%s' % (prefix, get_request_key(request))
                if cache.get(key):
                    response = HttpResponse('Please try again later.')
                    response.status_code = 503
                    response['Retry-After'] = duration
                    return response
                else:
                    cache.set(key, True, duration)
            return function(request, *args, **kwargs)
        return inner
    return decorator
