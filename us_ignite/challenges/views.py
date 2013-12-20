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


def get_entry_or_404(challenge_slug, app_slug):
    query_kwargs = {
        'challenge__status': Challenge.PUBLISHED,
        'challenge__slug__exact': challenge_slug,
        'application__status': Application.PUBLISHED,
        'application__slug__exact': app_slug
    }
    related = ['challenge', 'application', 'application__user']
    try:
        entry = Entry.objects.select_related(*related).get(**query_kwargs)
    except Entry.DoesNotExist:
        raise Http404('Entry does not exist.')
    return entry


@login_required
def entry_detail(request, challenge_slug, app_slug):
    """Detail of the ``Entry`` to a ``Challenge``

    The ``Challenge`` and the ``Application`` must be published.

    """
    entry = get_entry_or_404(challenge_slug, app_slug)
    is_owner = entry.application.is_owned_by(request.user)
    # Make sure the entry is available to this user:
    if not entry.is_visible_by(request.user):
        raise Http404('Entry is not published.')
    # When the challenge has not finished entries might be hidden:
    if not entry.challenge.has_finished():
        if entry.challenge.hide_entries and not is_owner:
            raise Http404('Entry is not public yet.')
    answer_list = (entry.entryanswer_set.select_related('question').all()
                   .order_by('question__order'))
    context = {
        'challenge': entry.challenge,
        'application': entry.application,
        'entry': entry,
        'answer_list': answer_list,
        'is_owner': is_owner,
    }
    return TemplateResponse(request, 'challenges/entry_detail.html', context)


@login_required
def challenge_entry(request, challenge_slug, app_slug):
    """Entry form for an ``Application`` for a given ``Challenge``.

    The ``Challenge`` has a list of ``Questions`` that will be translated
    into a ``ChallengeForm``."""
    # Application must be owned by the user:
    application = get_object_or_404(
        Application, slug__exact=app_slug, owner=request.user,
        status=Application.PUBLISHED)
    # Challenge must be open:
    challenge = get_object_or_404(
        Challenge, slug__exact=challenge_slug, status=Challenge.PUBLISHED)
    if not challenge.is_open():
        return redirect('entry_detail', challenge_slug, app_slug)
    # Determine if an entry already exists:
    entry = Entry.objects.get_entry_or_none(challenge, application)
    ChallengeForm = forms.get_challenge_form(challenge)
    if request.method == 'POST':
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
