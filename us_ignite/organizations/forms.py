from django import forms

from us_ignite.organizations.models import Organization


class OrganizationForm(forms.ModelForm):

    class Meta:
        fields = ('name', 'bio', 'image', 'website', 'tags')
        model = Organization
