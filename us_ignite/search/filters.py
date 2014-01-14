from django.template.response import TemplateResponse
from django.shortcuts import _get_queryset as get_queryset

from us_ignite.common import pagination
from us_ignite.search.forms import TagSearchForm


def tag_search(request, klass, template):
    # Generate a queryset from a model, manager or queryset:
    form = TagSearchForm(request.GET)
    page_no = pagination.get_page_no(request.GET)
    if form.is_valid():
        queryset = get_queryset(klass)
        object_list = queryset.filter(tags__name=form.cleaned_data['tag'])
    else:
        object_list = []
    page = pagination.get_page(object_list, page_no)
    context = {
        'page': page,
        'form': form,
    }
    return TemplateResponse(request, template, context)
