import pytz
import requests

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime

from us_ignite.blog.models import Post


URL = '%s/api/get_recent_posts/' % settings.WP_URL
# Timezone used to generate the Posts:
WP_TIMEZONE = 'America/New_York'


def parse_date(date_string):
    """Parse the date with the following format ``2014-01-13 16:05:47``"""
    naive = parse_datetime(date_string)
    return pytz.timezone(WP_TIMEZONE).localize(naive, is_dst=None)


def get_author(author_data):
    return User.objects.get(email='alfredo@madewithbyt.es')


def import_post(post_data):
    wp_id = post_data['id']
    try:
        post = Post.objects.get(wp_id__exact=wp_id)
    except Post.DoesNotExist:
        # Publish the post the first time it is imported:
        post = Post(wp_id=wp_id, status=Post.PUBLISHED)
    post.wp_type = post_data['type']
    post.title = post_data['title']
    post.slug = post_data['slug']
    post.content = post_data['content']
    post.excerpt = post_data['excerpt']
    post.author = get_author(post_data['author'])
    post.publication_date = parse_date(post_data['date'])
    post.update_date = parse_date(post_data['modified'])
    post.save()
    return post


def consume(extra_data=None):
    extra_data = extra_data if extra_data else {}
    response = requests.get(URL, data=extra_data)
    results = response.json()
    pages = results.get('pages', 0)
    post_list = []
    for post_data in results.get('posts', []):
        post = import_post(post_data)
        post_list.append(post)
    return post_list
