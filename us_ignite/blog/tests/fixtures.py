from us_ignite.profiles.tests.fixtures import get_user
from us_ignite.blog.models import Entry


def get_entry(**kwargs):
    data = {
        'slug': 'gigabit',
        'title': 'Gigabit!',
        'body': 'Lorem Ipsum',
    }
    if not 'author' in kwargs:
        data['author'] = get_user('us-ignite')
    data.update(kwargs)
    return Entry.objects.create(**data)
