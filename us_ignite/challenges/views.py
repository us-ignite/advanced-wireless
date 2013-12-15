from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.utils import timezone

from us_ignite.apps.models import Application
from us_ignite.challenges import forms
from us_ignite.challenges.models import Challenge, Entry


def challenge_list(request):
    now = timezone.now()
    object_list = Challenge.objects.filter(
        end_datetime__gte=now, status=Challenge.PUBLISHED)
    context = {
        'object_list': object_list,
    }
    return TemplateResponse(request, 'challenges/object_list.html', context)


def challenge_detail(request, slug):
    challenge = get_object_or_404(
        Challenge.active, slug__exact=slug, status=Challenge.PUBLISHED)
    entry_list = []
    if request.user.is_authenticated():
        application_list = Application.objects.filter(
            owner=request.user, status=Application.PUBLISHED)
        if application_list:
            entry_list = Entry.objects.get_entries_for_apps(
                challenge, application_list)
    context = {
        'object': challenge,
        'entry_list': entry_list,
    }
    return TemplateResponse(request, 'challenges/object_detail.html', context)


def entry_detail(request, challenge_slug, app_slug):
    """Detail of the ``Entry`` to a ``Challenge`` """
    challenge = get_object_or_404(Challenge.active, slug__exact=challenge_slug)
    application = get_object_or_404(
        Application.active, slug__exact=app_slug, owner=request.user,
        status=Application.PUBLISHED)
    entry = Entry.objects.get_entry_or_none(challenge, application)
    if not entry:
        raise Http404
    answer_list = (entry.entryanswer_set.select_related('question').all()
                   .order_by('question__order'))
    context = {
        'challenge': challenge,
        'application': application,
        'entry': entry,
        'answer_list': answer_list,
    }
    return TemplateResponse(
        request, 'challenges/entry_detail.html', context)


@login_required
def challenge_entry(request, challenge_slug, app_slug):
    """Entry form for an ``Application`` for a given ``Challenge``.

    The ``Challenge`` has a list of ``Questions`` that will be translated
    into a ``ChallengeForm``.

    The ``owner`` of the ``Application`` can save the progress on the entry
    decide when it's ready to participate.

    Once the entry has been marked as ``SUBMITTED`` or has been
    ``ACCEPTED`` the page shows the detail of the entry, unless withdrawn,
    and the entry would require moderation again.
    """
    challenge = get_object_or_404(Challenge.active, slug__exact=challenge_slug)
    if not challenge.is_open():
        raise Http404
    application = get_object_or_404(
        Application.active, slug__exact=app_slug, owner=request.user,
        status=Application.PUBLISHED)
    # Generate a form from the questions in the admin:
    ChallengeForm = forms.get_challenge_form(challenge)
    entry = Entry.objects.get_entry_or_none(challenge, application)
    # Entry has been submitted, approved or rejected. Show detail:
    if entry and not entry.is_draft():
        return redirect(entry.get_absolute_url())
    if request.method == 'POST':
        # The entry is only created on a POST:
        entry, is_new = Entry.objects.get_or_create(
            challenge=challenge, application=application)
        form = ChallengeForm(request.POST)
        if form.is_valid():
            status = form.cleaned_data.pop('status')
            entry.status = status
            entry.save()
            entry.save_answers(form.cleaned_data)
            messages.success(request, 'Entry saved.')
            return redirect(
                'challenge_entry', challenge_slug=challenge.slug,
                app_slug=application.slug)
    else:
        args = [forms.get_challenge_initial_data(entry)] if entry else []
        form = ChallengeForm(*args)
    context = {
        'form': form,
        'challenge': challenge,
        'application': application,
        'entry': entry,
    }
    return TemplateResponse(request, 'challenges/object_entry.html', context)
