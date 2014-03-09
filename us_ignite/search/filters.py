import watson
from django.template.response import TemplateResponse
from django.shortcuts import _get_queryset as get_queryset

from us_ignite.common import pagination
from us_ignite.search.forms import TagSearchForm


def tag_search(request, klass, template):
    """Search subset of models with the given tag.

    Usess ``watson`` for the full-text search.
    """
    # Generate a queryset from a model, manager or queryset:
    form = TagSearchForm(request.GET)
    page_no = pagination.get_page_no(request.GET)
    if form.is_valid():
        queryset = get_queryset(klass)
        object_list = watson.search(
            form.cleaned_data['tag'], models=(queryset, ))
    else:
        object_list = []
    page = pagination.get_page(object_list, page_no)
    context = {
        'page': page,
        'form': form,
    }
    return TemplateResponse(request, template, context)
