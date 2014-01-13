from django import forms

from us_ignite.resources.models import Resource


def _get_status_choices():
    """Returns a list of valid user status for the ``Resource``"""
    available_status = [
        Resource.PUBLISHED,
        Resource.DRAFT,
    ]
    is_valid_status = lambda x: x[0] in available_status
    return filter(is_valid_status, Resource.STATUS_CHOICES)


class ResourceForm(forms.ModelForm):
    status = forms.ChoiceField(
        choices=_get_status_choices(), initial=Resource.DRAFT)

    class Meta:
        model = Resource
        fields = ('name', 'description', 'url', 'asset', 'tags')

    def clean(self):
        cleaned_data = self.cleaned_data
        if cleaned_data.get('asset') or cleaned_data.get('url'):
            return cleaned_data
        raise forms.ValidationError('An asset or an URL is required.')
