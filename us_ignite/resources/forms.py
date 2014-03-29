from django import forms
from django.contrib.auth.models import User


from us_ignite.common import output
from us_ignite.resources.models import Resource


def _get_status_choices():
    """Returns a list of valid user status for the ``Resource``"""
    available_status = [
        Resource.PUBLISHED,
        Resource.DRAFT,
    ]
    is_valid_status = lambda x: x[0] in available_status
    return filter(is_valid_status, Resource.STATUS_CHOICES)


def _validate_email(email):
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise forms.ValidationError('User is not registered.')
    return user


class ResourceForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=_get_status_choices(), initial=Resource.PUBLISHED)

    def clean_tags(self):
        if 'tags' in self.cleaned_data:
            return output.prepare_tags(self.cleaned_data['tags'])

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('asset') or cleaned_data.get('url'):
            return cleaned_data
        raise forms.ValidationError('An asset or an URL is required.')

    class Meta:
        model = Resource
        fields = ('name', 'status', 'description', 'url', 'asset',
                  'resource_type', 'sector', 'author', 'organization',
                  'image', 'resource_date', 'tags')
