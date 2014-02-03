from us_ignite.maps.models import Category, Location


def get_category(**kwargs):
    data = {
        'name': 'Gigabit Network',
        'slug': 'gigabit-network',
    }
    data.update(kwargs)
    return Category.objects.create(**data)


def get_location(**kwargs):
    data = {
        'name': 'Gigabit Hub',
    }
    if not 'category' in kwargs:
        data['category'] = get_category()
    data.update(kwargs)
    return Location.objects.create(**data)
