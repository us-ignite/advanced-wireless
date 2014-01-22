import pytz
import requests

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.dateparse import parse_datetime

from us_ignite.blog.models import Post, PostAttachment


URL = '%s/api/get_recent_posts/' % settings.WP_URL
# Timezone used to generate the Posts:
WP_TIMEZONE = 'America/New_York'
POST_COUNT = 1000


def parse_date(date_string):
    """Parse the date with the following format ``2014-01-13 16:05:47``"""
    naive = parse_datetime(date_string)
    return pytz.timezone(WP_TIMEZONE).localize(naive, is_dst=None)


def get_author(author_data):
    # TODO: Use a proper user:
    return User.objects.get(email='alfredo@madewithbyt.es')


def import_attachment(post, data):
    wp_id = data['id']
    try:
        return PostAttachment.objects.get(post=post, wp_id__exact=wp_id)
    except PostAttachment.DoesNotExist:
        pass
    attachment = PostAttachment(post=post, wp_id=wp_id)
    attachment.title = data['title']
    attachment.slug = data['slug']
    attachment.url = data['url']
    attachment.mime_type = data['mime_type']
    attachment.description = data['description']
    attachment.caption = data['caption']
    attachment.save()
    return attachment


def import_post(data):
    wp_id = data['id']
    try:
        post = Post.objects.get(wp_id__exact=wp_id)
    except Post.DoesNotExist:
        # Publish the post the first time it is imported:
        post = Post(wp_id=wp_id, status=Post.PUBLISHED)
    post.wp_type = data['type']
    post.title = data['title']
    post.slug = data['slug']
    post.content = data['content']
    post.excerpt = data['excerpt']
    post.author = get_author(data['author'])
    post.publication_date = parse_date(data['date'])
    post.update_date = parse_date(data['modified'])
    post.save()
    for attachment_data in data.get('attachments', []):
        attachment = import_attachment(post, attachment_data)
    return post


def consume(extra_data=None, count=POST_COUNT):
    data = {
        'count': count
    }
    if extra_data:
        data.update(extra_data)
    response = requests.get(URL, params=data)
    results = response.json()
    pages = results.get('pages', 0)
    post_list = []
    for post_data in results.get('posts', []):
        post = import_post(post_data)
        post_list.append(post)
    return post_list
