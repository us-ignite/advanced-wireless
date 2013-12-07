from django.shortcuts import get_object_or_404
from django.http import Http404
from django.template.response import TemplateResponse

from us_ignite.organizations.models import Organization


def organization_detail(request, slug):
    organization = get_object_or_404(Organization, slug__exact=slug)
    if not organization.is_visible_by(request.user):
        raise Http404
    context = {
        'object': organization,
    }
    return TemplateResponse(
        request, 'organizations/object_detail.html', context)
