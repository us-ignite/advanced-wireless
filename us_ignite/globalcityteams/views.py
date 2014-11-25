from us_ignite.blog.models import Post
from us_ignite.blog.views import (
    post_list as post_list_source,
    post_detail as post_detail_source,
)
from us_ignite.events.models import Event
from us_ignite.events.views import (
    event_list as event_list_source,
    event_detail as event_detail_source,
)
from us_ignite.search.views import search as search_source


def event_list(request):
    """List the events for the global city teams."""
    response = event_list_source(request, section=Event.GLOBALCITIES)
    response.template_name = 'globalcityteams/event_list.html'
    return response


def event_detail(request, slug):
    response = event_detail_source(request, slug, section=Event.GLOBALCITIES)
    response.template_name = 'globalcityteams/event_detail.html'
    return response


def search(request):
    """Search for the global city teams content."""
    response = search_source(request, 'globalcities')
    response.template_name = 'globalcityteams/search.html'
    return response


def post_list(request):
    """News for the global city teams"""
    response = post_list_source(request, section=Post.GLOBALCITIES)
    response.template_name = 'globalcityteams/news_list.html'
    return response


def post_detail(request, year, month, slug):
    """News detail the global city teams"""
    response = post_detail_source(
        request, year, month, slug, section=Post.GLOBALCITIES)
    response.template_name = 'globalcityteams/news_detail.html'
    return response
