import pytz
import requests
import HTMLParser

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.encoding import force_text
from django.utils.html import strip_tags
from django.utils.text import slugify
from django.utils.dateparse import parse_datetime

from us_ignite.common import sanitizer
from us_ignite.blog.models import Post, PostAttachment


URL = '%s/api/get_recent_posts/' % settings.WP_URL
# Timezone used to generate the Posts:
WP_TIMEZONE = 'America/New_York'
POST_COUNT = 1000


def parse_date(date_string):
    """Parse the date with the following format ``2014-01-13 16:05:47``"""
    naive = parse_datetime(date_string)
    return pytz.timezone(WP_TIMEZONE).localize(naive, is_dst=None)


def clean_stream(stream):
    parser = HTMLParser.HTMLParser()
    replacement_list = [
        ('<p></p>', ''),
    ]
    stream = unicode(parser.unescape(force_text(stream)))
    stream = sanitizer.sanitize(stream)
    for o, d in replacement_list:
        stream = stream.replace(o, d)
    return stream


def clean_excerpt(stream):
    """Clean the output text from an excerpt."""
    stream = strip_tags(clean_stream(stream))
    replacement_list = [
        (u'Continue reading ', ''),
        (u'\u2192', ''),
    ]
    for o, d in replacement_list:
        stream = stream.replace(o, d)
    return stream


def get_author(author_data):
    if not settings.WP_EMAIL:
        return None
    try:
        return User.objects.get(email=settings.WP_EMAIL)
    except User.DoesNotExist:
        return None


def import_attachment(post, data):
    wp_id = clean_stream(data['id'])
    try:
        return PostAttachment.objects.get(post=post, wp_id__exact=wp_id)
    except PostAttachment.DoesNotExist:
        pass
    attachment = PostAttachment(post=post, wp_id=wp_id)
    attachment.title = clean_stream(data['title'])
    attachment.slug = slugify(clean_stream(data['slug']))
    attachment.url = clean_stream(data['url'])
    attachment.mime_type = clean_stream(data['mime_type'])
    attachment.description = clean_stream(data['description'])
    attachment.caption = clean_stream(data['caption'])
    attachment.save()
    return attachment


def import_post(data):
    wp_id = data['id']
    try:
        post = Post.objects.get(wp_id__exact=wp_id)
    except Post.DoesNotExist:
        # Publish the post the first time it is imported:
        post = Post(wp_id=wp_id, status=Post.PUBLISHED)
    # Determine the author of the post, if existing:
    author = get_author(data['author'])
    if not post.author and author:
        post.author = author
    post.wp_type = clean_stream(data['type'])
    post.title = clean_stream(data['title'])
    post.slug = slugify(clean_stream(data['slug']))
    post.content = clean_stream(data['content'])
    post.content_html = post.content
    post.excerpt = clean_excerpt(data['excerpt'])
    post.excerpt_html = post.excerpt
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
