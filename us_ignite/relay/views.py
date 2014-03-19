from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse

from us_ignite.common.decorators import throttle_view
from us_ignite.profiles.models import Profile
from us_ignite.relay import forms, engine


@throttle_view(methods=['POST'], duration=30)
@login_required
def contact_user(request, slug):
    profile = get_object_or_404(
        Profile.active.select_related('user'), slug__exact=slug)
    if request.method == 'POST':
        form = forms.ContactForm(request.POST)
        if form.is_valid():
            context = {
                'title': form.cleaned_data['title'],
                'body': form.cleaned_data['body'],
                'sender': request.user,
                'destinatary': profile,
                'SITE_URL': settings.SITE_URL,
            }
            engine.contact_user(
                profile.display_email, request.user.email, context)
            messages.success(request, 'Message sent successfully.')
            return redirect(profile.get_absolute_url())
    else:
        form = forms.ContactForm()
    context = {
        'form': form,
        'object': profile,
    }
    return TemplateResponse(request, 'relay/contact_user.html', context)


@throttle_view(methods=['POST'], duration=30)
def contact_ignite(request):
    if request.method == 'POST':
        form = forms.ContactEmailForm(request.POST)
        if form.is_valid():
            context = {
                'title': form.cleaned_data['title'],
                'body': form.cleaned_data['body'],
                'SITE_URL': settings.SITE_URL,
                'email': form.cleaned_data['email']
            }
            engine.contact_user(
                settings.DEFAULT_FROM_EMAIL, form.cleaned_data['email'], context)
            messages.success(request, 'Message sent successfully.')
            return redirect('home')
    else:
        form = forms.ContactEmailForm()
    context = {
        'form': form,
    }
    return TemplateResponse(request, 'relay/contact_ignite.html', context)
