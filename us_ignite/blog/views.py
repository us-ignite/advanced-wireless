from django.http import Http404
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404

from us_ignite.blog.models import Entry


def entry_list(request):
    object_list = Entry.published.select_related('author').all()
    context = {
        'object_list': object_list,
    }
    return TemplateResponse(request, 'blog/object_list.html', context)


def entry_detail(request, year, month, slug):
    entry = get_object_or_404(
        Entry, slug=slug, publication_date__year=year,
        publication_date__month=month)
    if not entry.is_visible_by(request.user):
        raise Http404
    context = {
        'object': entry,
    }
    return TemplateResponse(request, 'blog/object_detail.html', context)
