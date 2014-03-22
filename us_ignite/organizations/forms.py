from django import forms

from us_ignite.common import output
from us_ignite.organizations.models import Organization

from us_ignite.profiles.models import Interest


class OrganizationForm(forms.ModelForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(), required=False,
        widget=forms.CheckboxSelectMultiple)

    def clean_tags(self):
        if 'tags' in self.cleaned_data:
            return output.prepare_tags(self.cleaned_data['tags'])

    class Meta:
        fields = ('name', 'bio', 'image', 'website', 'interest_ignite',
                  'interests', 'interests_other', 'resources_available',
                  'tags', 'position')
        model = Organization
