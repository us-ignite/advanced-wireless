import json

from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse


def json_response(data, callback=None):
    json_dump = json.dumps(data, cls=DjangoJSONEncoder)
    response = u'%s(%s)' % (callback, json_dump) if callback else json_dump
    return HttpResponse(response, content_type='application/javascript')
