from urlparse import urlparse, parse_qs

from django import forms
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.forms.models import inlineformset_factory
from django.utils import html

from us_ignite.actionclusters.models import (
    ActionCluster,
    ActionClusterURL,
    ActionClusterMedia,
    ActionClusterMembership,
)
from us_ignite.common import output


def _get_status_choices():
    """Returns a list of valid user status for the ``ActionCluster``"""
    available_status = [
        ActionCluster.PUBLISHED,
        ActionCluster.DRAFT,
    ]
    is_valid_status = lambda x: x[0] in available_status
    return filter(is_valid_status, ActionCluster.STATUS_CHOICES)


class ActionClusterForm(forms.ModelForm):
    """Model form for the ``ActionCluster`` with whitelisted fields."""
    status = forms.ChoiceField(
        choices=_get_status_choices(), initial=ActionCluster.DRAFT)
    summary = forms.CharField(
        max_length=140, widget=forms.Textarea,
        help_text='Tweet-length pitch / summary of project.')

    class Meta:
        model = ActionCluster
        fields = ('name', 'summary', 'impact_statement',
                  'image', 'domain', 'features', 'stage', 'needs_partner',
                  'assistance', 'team_name', 'team_description',
                  'awards', 'acknowledgments', 'tags', 'status',)
        widgets = {
            'features': forms.CheckboxSelectMultiple(),
        }

    def _strip_tags(self, field):
        if field in self.cleaned_data:
            return html.strip_tags(self.cleaned_data[field])

    def clean_team_description(self):
        return self._strip_tags('team_description')

    def clean_tags(self):
        if 'tags' in self.cleaned_data:
            return output.prepare_tags(self.cleaned_data['tags'])


ActionClusterLinkFormSet = inlineformset_factory(
    ActionCluster, ActionClusterURL, max_num=3, extra=3, can_delete=False, fields='__all__')


def is_embedable_url(url):
    domain_list = ['www.youtube.com']
    url_parsed = urlparse(url)
    if url_parsed.netloc.lower() in domain_list:
        query = parse_qs(url_parsed.query)
        return True if query.get('v') else False
    return False


class ActionClusterMediaForm(forms.ModelForm):

    def clean_url(self):
        url = self.cleaned_data.get('url')
        if url:
            if is_embedable_url(url):
                return url
            raise forms.ValidationError('Not valid URL.')
        return ''

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('url') or cleaned_data.get('image'):
            return self.cleaned_data
        raise forms.ValidationError('An image or a URL is required.')

    class Meta:
        fields = ('name', 'image', 'url')
        model = ActionClusterMedia


ActionClusterMediaFormSet = inlineformset_factory(
    ActionCluster, ActionClusterMedia, max_num=10, extra=1,
    can_delete=False, form=ActionClusterMediaForm)


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
        label=u'Team Members',
        widget=forms.Textarea, help_text=u'Add registered users as '
        'collaborators for this app. One email per line.', required=False)

    def clean_collaborators(self):
        """Validates the payload is a list of registered usernames."""
        collaborators_raw = self.cleaned_data.get('collaborators')
        member_list = []
        if collaborators_raw:
            collaborator_list = [c for c in collaborators_raw.splitlines() if c]
            for collaborator in collaborator_list:
                collaborator = collaborator.strip()
                member = validate_member(collaborator)
                member_list.append(member)
        return member_list


class ActionClusterMembershipForm(forms.ModelForm):

    class Meta:
        model = ActionClusterMembership
        fields = ('can_edit', )


ActionClusterMembershipFormSet = inlineformset_factory(
    ActionCluster, ActionClusterMembership, extra=0, max_num=0,
    form=ActionClusterMembershipForm)
