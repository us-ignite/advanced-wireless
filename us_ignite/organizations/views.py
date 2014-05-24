from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from us_ignite.common import pagination
from us_ignite.organizations.forms import OrganizationForm
from us_ignite.organizations.models import Organization


def organization_detail(request, slug):
    organization = get_object_or_404(Organization, slug__exact=slug)
    if not organization.is_visible_by(request.user):
        raise Http404
    interest_list = [i.name for i in organization.interests.all()]
    if organization.interests_other:
        interest_list += [organization.interests_other]
    context = {
        'object': organization,
        'member_list': organization.members.all(),
        'is_member': organization.is_member(request.user),
        'interest_list': interest_list,
    }
    return TemplateResponse(
        request, 'organizations/object_detail.html', context)


@login_required
def organization_edit(request, slug):
    organization = get_object_or_404(
        Organization, slug__exact=slug, members=request.user)
    if request.method == 'POST':
        form = OrganizationForm(request.POST, instance=organization)
        if form.is_valid():
            instance = form.save()
            message = 'Organization "%s" has been updated.' % instance.name
            messages.success(request, message)
            return redirect(instance.get_absolute_url())
    else:
        form = OrganizationForm(instance=organization)
    context = {
        'object': organization,
        'form': form,
    }
    return TemplateResponse(request, 'organizations/object_edit.html', context)


def organization_list(request):
    page_no = pagination.get_page_no(request.GET)
    object_list = Organization.active.all()
    page = pagination.get_page(object_list, page_no)
    context = {
        'page': page,
    }
    return TemplateResponse(request, 'organizations/object_list.html', context)
