from django.conf import settings
from django.http import HttpResponse


def basic_challenge(realm=None):
    if realm is None:
        realm = getattr(settings, 'WWW_AUTHENTICATION_REALM',
                        'Restricted Access')
    response = HttpResponse('Authorization Required', mimetype="text/plain")
    response['WWW-Authenticate'] = 'Basic realm="%s"' % (realm)
    response.status_code = 401
    return response


def _get_setting(key):
    return getattr(settings, 'BASIC_WWW_AUTHENTICATION_%s' % key)


def basic_authenticate(authentication):
    # Taken from paste.auth
    authmeth, auth = authentication.split(' ', 1)
    if 'basic' != authmeth.lower():
        return None
    auth = auth.strip().decode('base64')
    username, password = auth.split(':', 1)
    USERNAME = _get_setting('USERNAME')
    PASSWORD = _get_setting('PASSWORD')
    return username == USERNAME and password == PASSWORD


class BasicAuthenticationMiddleware(object):
    def process_request(self, request):
        if not getattr(settings, 'BASIC_WWW_AUTHENTICATION', False):
            return
        if 'HTTP_AUTHORIZATION' not in request.META:
            return basic_challenge()
        authenticated = basic_authenticate(request.META['HTTP_AUTHORIZATION'])
        if authenticated:
            return
        return basic_challenge()
