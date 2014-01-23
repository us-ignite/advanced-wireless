from mock import Mock, patch
from nose.tools import assert_raises, eq_

from django.http import Http404
from django.test import TestCase

from us_ignite.common.tests import utils
from us_ignite.blog import views
from us_ignite.blog.models import Post


patch_get_object = patch('us_ignite.blog.views.get_object_or_404')


class TestPostListView(TestCase):

    @patch('us_ignite.blog.models.Post.published.select_related')
    def test_request_is_successful(self, related_mock):
        request = utils.get_request('get', '/blog/', user=utils.get_anon_mock())
        response = views.post_list(request)
        eq_(response.status_code, 200)
        eq_(response.template_name, 'blog/object_list.html')
        eq_(sorted(response.context_data.keys()), ['object_list'])
        related_mock.assert_called_once_with('author')


class TestPostDetailView(TestCase):

    @patch_get_object
    def test_invalid_published_post_returns_404(self, mock_get):
        mock_get.side_effect = Http404
        request = utils.get_request('get', '/blog/', user=utils.get_anon_mock())
        assert_raises(Http404, views.post_detail, request, 2013, 12, 'gigabit')
        mock_get.assert_called_once_with(
            Post, slug='gigabit', publication_date__year=2013,
            publication_date__month=12)

    @patch_get_object
    def test_not_visible_post_raises_404(self, mock_get):
        mock_post = Mock(spec=Post)()
        mock_post.is_visible_by.return_value = False
        mock_get.return_value = mock_post
        user = utils.get_anon_mock()
        request = utils.get_request('get', '/blog/', user=user)
        assert_raises(Http404, views.post_detail, request, 2013, 12, 'gigabit')
        mock_get.assert_called_once_with(
            Post, slug='gigabit', publication_date__year=2013,
            publication_date__month=12)
        mock_post.is_visible_by.assert_called_once_with(user)

    @patch_get_object
    def test_published_post_request_is_successful(self, mock_get):
        mock_post = Mock(spec=Post)()
        mock_post.is_visible_by.return_value = True
        mock_get.return_value = mock_post
        request = utils.get_request('get', '/blog/', user=utils.get_anon_mock())
        response = views.post_detail(request, 2013, 12, 'gigabit')
        eq_(response.status_code, 200)
        eq_(response.template_name, 'blog/object_detail.html')
        eq_(sorted(response.context_data.keys()), ['object'])
        mock_get.assert_called_once_with(
            Post, slug='gigabit', publication_date__year=2013,
            publication_date__month=12)
        mock_post.is_visible_by.assert_called_once_with(request.user)


class TestLegacyRedirectView(TestCase):

    @patch_get_object
    def test_redirect_does_not_exists(self, mock_get):
        mock_get.side_effect = Http404
        request = utils.get_request('get', '/2014/3/foo/')
        assert_raises(Http404, views.legacy_redirect, request, 2014, 3, u'foo')
        mock_get.assert_called_once_with(
            Post.published, slug='foo', publication_date__year=2014,
            publication_date__month=3)

    @patch_get_object
    def test_legacy_redirect_exists(self, mock_get):
        mock_instance = Mock(spec=Post)
        mock_instance.get_absolute_url.return_value = '/blog/2014/3/foo/'
        mock_get.return_value = mock_instance
        request = utils.get_request('get', '/2014/3/foo/')
        response = views.legacy_redirect(request, 2014, 3, u'foo')
        eq_(response.status_code, 301)
        eq_(response['Location'], '/blog/2014/3/foo/')
        mock_get.assert_called_once_with(
            Post.published, slug='foo', publication_date__year=2014,
            publication_date__month=3)
