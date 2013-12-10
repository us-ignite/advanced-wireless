from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils import timezone

from us_ignite.apps.models import Application
from us_ignite.challenges import forms
from us_ignite.challenges.models import Challenge, Entry, EntryAnswer, Question


def challenge_list(request):
    now = timezone.now()
    object_list = Challenge.objects.filter(
        end_datetime__gte=now, status=Challenge.PUBLISHED)
    context = {
        'object_list': object_list,
    }
    return TemplateResponse(request, 'challenges/object_list.html', context)


def get_entry(challenge, application):
    try:
        entry = Entry.objects.get(challenge=challenge, application=application)
    except Entry.DoesNotExist:
        entry = None
    return entry


@login_required
def challenge_entry(request, challenge_slug, app_slug):
    challenge = get_object_or_404(Challenge.active, slug__exact=challenge_slug)
    application = get_object_or_404(
        Application.active, slug__exact=app_slug, owner=request.user,
        status=Application.PUBLISHED)
    # Generate a form from the questions in the admin:
    ChallengeForm = forms.get_challenge_form(challenge)
    entry, is_new = Entry.objects.get_or_create(
        challenge=challenge, application=application)
    # TODO: determine what happens after the entry has been accepted.
    if request.method == 'POST':
        form = ChallengeForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data.pop('status')
            entry.status = status
            entry.save()
            answers = entry.save_answers(form.cleaned_data)
            messages.success(request, 'Entry saved.')
            return redirect(
                'challenge_entry', challenge_slug=challenge.slug,
                app_slug=application.slug)
    else:
        entry = get_entry(challenge, application)
        args = [forms.get_challenge_initial_data(entry)] if entry else []
        form = ChallengeForm(*args)
    context = {
        'form': form,
        'challenge': challenge,
        'application': application,
        'entry': entry,
    }
    return TemplateResponse(request, 'challenges/object_entry.html', context)
