from django.template.response import TemplateResponse

from us_ignite.common.response import json_response
from us_ignite.maps.models import Location


def location_list(request):
    """Shows a list of locations in a map."""
    object_list = Location.published.select_related('category').all()
    context = {
        'object_list': object_list,
    }
    return TemplateResponse(request, 'maps/object_list.html', context)


def _get_content(name, website):
    if not website:
        return name
    return u'<div><h2><a href="%s">%s</a></h2></div>' % (website, name)


def _get_location_data(location):
    return {
        'type': 'location',
        'latitude': location.position.latitude,
        'longitude': location.position.longitude,
        'name': location.name,
        'website': location.website,
        'category': location.category.name,
        'image': location.get_image_url(),
        'content': _get_content(location.name, location.website),
    }


def location_list_json(request):
    """Returns the locations in JSON format"""
    object_list = Location.published.select_related('category').all()
    dict_list = [_get_location_data(l) for l in object_list]
    return json_response(dict_list, callback='map.render')
