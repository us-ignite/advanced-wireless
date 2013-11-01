import functools

from django.contrib.auth.views import redirect_to_login
from django.http import HttpResponseRedirect
from django.shortcuts import render


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
                    return render(request, 'unavailable.html', {})
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
