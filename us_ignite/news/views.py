from django.template.response import TemplateResponse

from us_ignite.common import pagination
from us_ignite.news.models import Article


def article_list(request, section=Article.DEFAULT):
    page_no = pagination.get_page_no(request.GET)
    kwargs = {'section': section} if section else {}
    object_list = Article.published.filter(**kwargs)
    page = pagination.get_page(object_list, page_no)
    context = {
        'page': page,
    }
    return TemplateResponse(request, 'news/object_list.html', context)
