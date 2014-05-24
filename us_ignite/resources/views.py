from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from us_ignite.common import pagination
from us_ignite.resources.forms import ResourceForm
from us_ignite.resources.models import Resource


def resource_detail(request, slug):
    resource = get_object_or_404(Resource, slug__exact=slug)
    if not resource.is_visible_by(request.user):
        raise Http404
    context = {
        'object': resource,
        'is_owner': resource.is_editable_by(request.user)
    }
    return TemplateResponse(request, 'resources/object_detail.html', context)


def resource_list(request):
    page_no = pagination.get_page_no(request.GET)
    object_list = Resource.published.all()
    page = pagination.get_page(object_list, page_no)
    featured_list = Resource.published.filter(is_featured=True)[:3]
    context = {
        'page': page,
        'featured_list': featured_list,
    }
    return TemplateResponse(request, 'resources/object_list.html', context)


@login_required
def resource_add(request):
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.contact = request.user
            if form.cleaned_data.get('author'):
                instance.author = form.cleaned_data['author']
            instance.save()
            form.save_m2m()
            return redirect(instance.get_absolute_url())
    else:
        form = ResourceForm()
    context = {
        'form': form,
    }
    return TemplateResponse(request, 'resources/object_add.html', context)


@login_required
def resource_edit(request, slug):
    resource = get_object_or_404(Resource, slug__exact=slug)
    if not resource.is_editable_by(request.user):
        raise Http404
    if request.method == 'POST':
        form = ResourceForm(request.POST, request.FILES, instance=resource)
        if form.is_valid():
            instance = form.save()
            if form.cleaned_data.get('author'):
                instance.author = form.cleaned_data['author']
                instance.save()
            return redirect(instance.get_absolute_url())
    else:
        form = ResourceForm(instance=resource)
    context = {
        'form': form,
        'object': resource,
    }
    return TemplateResponse(request, 'resources/object_edit.html', context)
