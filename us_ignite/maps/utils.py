def get_location_dict(item, location_type):
    return {
        'type': location_type,
        'latitude': item.position.latitude,
        'longitude': item.position.longitude,
        'name': item.name,
        'website': item.get_absolute_url(),
        'category': '',
        'image': '',
        'content': item.name,
    }
