from us_ignite.snippets.models import Snippet


def get_snippet(**kwargs):
    data = {
        'name': 'Gigabit snippets',
        'slug': 'featured',
        'url': 'http://us-ignite.org/',
        'image': 'ad.png',
    }
    data.update(kwargs)
    return Snippet.objects.create(**data)
