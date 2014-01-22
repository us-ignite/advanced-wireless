from datetime import datetime
from mock import Mock, patch
from nose.tools import eq_, ok_

from django.contrib.auth.models import User
from django.test import TestCase

from us_ignite.blog import consumer
from us_ignite.blog.models import Post, PostAttachment


class TestParseDateFunction(TestCase):

    def test_date_is_parsed_correctly(self):
        date_string = '2014-01-13 16:05:47'
        date = consumer.parse_date(date_string)
        ok_(isinstance(date, datetime))
        eq_(date.tzinfo.zone, 'America/New_York')
        eq_(date.year, 2014)
        eq_(date.month, 1)
        eq_(date.day, 13)
        eq_(date.hour, 16)
        eq_(date.minute, 5)


def _get_post_data(**kwargs):
    data = {
        'id': 23,
        'type': 'post',
        'title': 'Gigabit Post',
        'slug': 'gigabit-post',
        'content': 'Content',
        'excerpt': 'Excerpt',
        'author': {},
        'date': '2014-01-13 16:05:47',
        'modified': '2014-01-13 16:05:47',
    }
    data.update(kwargs)
    return data


class TestImportPostFunction(TestCase):

    @patch.object(Post, 'save')
    @patch('us_ignite.blog.consumer.get_author')
    def test_post_is_imported_correctly(self, mock_get, mock_save):
        user = User(username='foo', id=2)
        mock_get.return_value = user
        data = _get_post_data()
        post = consumer.import_post(data)
        mock_save.assert_called_once_with()
        eq_(post.wp_id, 23)
        eq_(post.author, user)
        eq_(post.wp_type, 'post')
        eq_(post.title, 'Gigabit Post')
        eq_(post.content, 'Content')
        eq_(post.excerpt, 'Excerpt')
        ok_(post.publication_date)
        ok_(post.update_date)


class TestConsumeFunction(TestCase):

    @patch('us_ignite.blog.consumer.import_post')
    @patch('requests.get')
    def test_consumer_is_executed_successfully(self, mock_get, mock_import):
        response_mock = Mock()
        response_mock.json.return_value = {}
        mock_get.return_value = response_mock
        post_list = consumer.consume()
        mock_get.assert_called_once_with(
            'http://us-ignite.org/api/get_recent_posts/',
            params={'count': 1000})
        response_mock.json.assert_called_once_with()
        eq_(mock_import.call_count, 0)
        eq_(post_list, [])


def _get_attachment_data(**kwargs):
    data = {
        'id': 3367,
        'title': 'Image',
        'slug': 'image',
        'url': 'http://us-ignite.org/image.jpg',
        'mime_type': 'image/jpeg',
        'description': '',
        'caption': '',
    }
    data.update(kwargs)
    return data


class TestImportAttachmentFunction(TestCase):

    @patch.object(PostAttachment, 'save')
    def test_attachment_is_created_successfully(self, mock_save):
        data = _get_attachment_data()
        mock_post = Post()
        attachment = consumer.import_attachment(mock_post, data)
        eq_(attachment.wp_id, 3367)
        eq_(attachment.title, 'Image')
        eq_(attachment.slug, 'image')
        eq_(attachment.url, 'http://us-ignite.org/image.jpg')
        eq_(attachment.mime_type, 'image/jpeg')
        eq_(attachment.description, '')
        eq_(attachment.caption, '')
        eq_(attachment.post, mock_post)
        mock_save.assert_called_once_with()
