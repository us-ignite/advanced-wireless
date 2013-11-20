from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.forms.models import inlineformset_factory

from us_ignite.apps.models import (Application, ApplicationURL,
                                   ApplicationImage)


def _get_status_choices():
    """Returns a list of valid user status for the ``Application``"""
    available_status = [
        Application.PUBLISHED,
        Application.DRAFT,
        Application.PRIVATE,
    ]
    is_valid_status = lambda x: x[0] in available_status
    return filter(is_valid_status, Application.STATUS_CHOICES)


class ApplicationForm(forms.ModelForm):
    """Model form for the ``Application`` with whitelisted fields."""
    status = forms.ChoiceField(
        choices=_get_status_choices(), initial=Application.DRAFT)
    summary = forms.CharField(
        max_length=140, widget=forms.Textarea,
        help_text='Tweet-length pitch / summary of project.')

    class Meta:
        model = Application
        fields = ('name', 'summary', 'impact_statement', 'description',
                  'image', 'domain',  'features', 'stage', 'roadmap',
                  'assistance', 'team_description', 'acknowledgments',
                  'tags', 'status',)


ApplicationLinkFormSet = inlineformset_factory(
    Application, ApplicationURL, max_num=3, extra=3)


ApplicationImageFormSet = inlineformset_factory(
    Application, ApplicationImage, max_num=10, extra=1)


def validate_member(email):
    """Validates the user has a valid email and it is registered."""
    try:
        validate_email(email)
    except forms.ValidationError:
        raise forms.ValidationError(
            '``%s`` is an invalid email address.' % email)
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        raise forms.ValidationError(
            'User with ``%s`` email is not registered.' % email)


class MembershipForm(forms.Form):
    """Form to validate the collaborators."""
    collaborators = forms.CharField(
        widget=forms.Textarea, help_text='Add registered users as '
        'collaborators for this app. One email per line.')

    def clean_collaborators(self):
        """Validates the payload is a list of registered usernames."""
        collaborators_raw = self.cleaned_data.get('collaborators')
        if collaborators_raw:
            member_list = []
            collaborator_list = [c for c in collaborators_raw.splitlines() if c]
            for collaborator in collaborator_list:
                collaborator = collaborator.strip()
                member = validate_member(collaborator)
                member_list.append(member)
            return member_list
