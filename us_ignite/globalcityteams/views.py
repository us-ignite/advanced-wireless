from us_ignite.events.models import Event
from us_ignite.events.views import event_list as event_list_source
from us_ignite.news.models import Article
from us_ignite.news.views import article_list as article_list_source
from us_ignite.search.views import search as search_source


def event_list(request):
    """List the events for the global city teams."""
    response = event_list_source(request, section=Event.GLOBALCITIES)
    response.template_name = 'globalcityteams/event_list.html'
    return response


def article_list(request):
    """List the news for the global city teams"""
    response = article_list_source(request, section=Article.GLOBALCITIES)
    response.template_name = 'globalcityteams/article_list.html'
    return response


def search(request):
    response = search_source(request, 'globalcities')
    return response
