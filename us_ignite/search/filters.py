import watson
from django.template.response import TemplateResponse
from django.shortcuts import _get_queryset as get_queryset
from django.utils.http import urlencode

from us_ignite.common import pagination
from us_ignite.search.forms import SearchForm


def tag_search(request, klass, template):
    """Search subset of models with the given tag.

    Usess ``watson`` for the full-text search.
    """
    # Generate a queryset from a model, manager or queryset:
    form = SearchForm(request.GET)
    page_no = pagination.get_page_no(request.GET)
    if form.is_valid():
        queryset = get_queryset(klass)
        object_list = watson.search(
            form.cleaned_data['q'], models=(queryset, ))
        pagination_qs = '&%s' % urlencode({'q': form.cleaned_data['q']})
    else:
        object_list = []
        pagination_qs = ''
    page = pagination.get_page(object_list, page_no)
    page.object_list_top = [o.object for o in page.object_list_top]
    page.object_list_bottom = [o.object for o in page.object_list_bottom]
    context = {
        'page': page,
        'form': form,
        'pagination_qs': pagination_qs,
    }
    return TemplateResponse(request, template, context)
