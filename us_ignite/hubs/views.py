from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template.response import TemplateResponse
from django.shortcuts import get_object_or_404, redirect

from us_ignite.hubs.models import Hub, HubRequest
from us_ignite.hubs import forms, mailer


@login_required
def hub_application(request):
    """View to submit a ``Hub`` for consideration"""
    object_list = HubRequest.objects.filter(
        ~Q(status=HubRequest.REMOVED), user=request.user)
    if request.method == 'POST':
        form = forms.HubRequestForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.user = request.user
            instance.save()
            # Notify US Ignite about this request:
            mailer.notify_request(instance)
            msg = 'The registration for "%s" has been submited.' % instance.name
            messages.success(request, msg)
            return redirect('home')
    else:
        form = forms.HubRequestForm()
    context = {
        'form': form,
        'object_list': object_list,
    }
    return TemplateResponse(request, 'hubs/object_application.html', context)


def hub_detail(request, slug):
    """Homepage of a Ignite Community.

    This view aggregates all the content related to this ``Hub``.
    """
    instance = get_object_or_404(Hub, slug=slug)
    if not instance.is_published() and not instance.is_guardian(request.user):
        raise Http404
    context = {
        'object': instance,
    }
    return TemplateResponse(request, 'hubs/object_detail.html', context)
