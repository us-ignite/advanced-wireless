from __future__ import division
import math
import random

# Geographic centre of the USA:
longitude = float(39.8281418)
latitude = float(-98.6419404)


def get_location(radius=90):
    lng_min = longitude - radius / abs(math.cos(math.radians(latitude)) * 69)
    lng_max = longitude + radius / abs(math.cos(math.radians(latitude)) * 69)
    lat_min = latitude - (radius / 69)
    lat_max = latitude + (radius / 69)
    lng = random.triangular(lng_min, lng_max)
    lat = random.triangular(lat_min, lat_max)
    return [lng, lat]
