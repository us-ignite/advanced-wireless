from us_ignite.news.models import Article


def get_article(**kwargs):
    data = {
        'name': 'Gigabit news',
        'url': 'http://us-ignite.org/',
    }
    data.update(kwargs)
    return Article.objects.create(**data)
