import urlparse
from django.http import HttpResponsePermanentRedirect
from django.conf import settings


class DoNotTrackMiddleware(object):

    def process_request(self, request):
        request.is_dnt = request.META.get('HTTP_DNT') == '1'


class URLRedirectMiddleware(object):
    """Redirects an invalid HOST URL to the expected domain."""

    def process_request(self, request):
        host = request.META.get('HTTP_HOST', '')
        parsed_url = urlparse.urlparse(settings.SITE_URL)
        if not settings.DEBUG and not host == parsed_url.netloc:
            new_url = settings.SITE_URL + request.path_info
            return HttpResponsePermanentRedirect(new_url)
