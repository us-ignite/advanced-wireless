from us_ignite.profiles.tests.fixtures import get_user
from us_ignite.blog.models import Post


def get_post(**kwargs):
    data = {
        'slug': 'gigabit',
        'title': 'Gigabit!',
    }
    if not 'author' in kwargs:
        data['author'] = get_user('us-ignite')
    data.update(kwargs)
    return Post.objects.create(**data)
