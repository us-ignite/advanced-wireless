from us_ignite.awards.models import Award


def get_award(**kwargs):
    data = {
        'name': 'Gold star!',
    }
    return Award.objects.create(**data)
