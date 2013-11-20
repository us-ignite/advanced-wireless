from us_ignite.badges.models import Badge


def get_badge(**kwargs):
    data = {
        'name': 'Gold star!',
    }
    return Badge.objects.create(**data)
