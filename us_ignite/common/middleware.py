class DoNotTrackMiddleware(object):

    def process_request(self, request):
        request.is_dnt = request.META.get('HTTP_DNT') == '1'
