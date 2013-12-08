from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from us_ignite.organizations.forms import OrganizationForm
from us_ignite.organizations.models import Organization


def organization_detail(request, slug):
    organization = get_object_or_404(Organization, slug__exact=slug)
    if not organization.is_visible_by(request.user):
        raise Http404
    context = {
        'object': organization,
        'member_list': organization.members.all(),
        'is_member': organization.is_member(request.user),
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
