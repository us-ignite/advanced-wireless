from django.http import Http404
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect
from django.utils.text import slugify

from us_ignite.blog.models import Post
from us_ignite.common import pagination


def post_list(request):
    """List the published ``Posts``"""
    page_no = pagination.get_page_no(request.GET)
    featured_list = (Post.published.select_related('author')
                     .filter(is_featured=True)[:3])
    object_list = Post.published.select_related('author').all()
    page = pagination.get_page(object_list, page_no)
    context = {
        'page': page,
        'featured_list': featured_list,
    }
    return TemplateResponse(request, 'blog/object_list.html', context)


def post_detail(request, year, month, slug):
    post = get_object_or_404(
        Post, slug=slug, publication_date__year=year,
        publication_date__month=month)
    if not post.is_visible_by(request.user):
        raise Http404
    context = {
        'object': post,
    }
    return TemplateResponse(request, 'blog/object_detail.html', context)


def legacy_redirect(request, year, month, slug):
    """Redirects a legacy published ``Post`` to the new URL."""
    slug = slugify(slug)
    post = get_object_or_404(
        Post.published, slug=slug, publication_date__year=year,
        publication_date__month=month)
    if post:
        return redirect(post.get_absolute_url(), permanent=True)
    raise Http404('Does not exist.')
