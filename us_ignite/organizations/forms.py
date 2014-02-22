from django import forms

from us_ignite.common import output
from us_ignite.organizations.models import Organization


class OrganizationForm(forms.ModelForm):

    def clean_tags(self):
        if 'tags' in self.cleaned_data:
            return output.prepare_tags(self.cleaned_data['tags'])

    class Meta:
        fields = ('name', 'bio', 'image', 'website', 'tags', 'position')
        model = Organization
