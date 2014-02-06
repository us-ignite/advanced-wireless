from us_ignite.advertising.models import Advert


def get_advert(**kwargs):
    data = {
        'name': 'Gigabit advertising',
        'url': 'http://us-ignite.org/',
        'image': 'ad.png',
    }
    data.update(kwargs)
    return Advert.objects.create(**data)
