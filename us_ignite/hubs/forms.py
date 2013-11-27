from django import forms

from us_ignite.hubs.models import HubRequest


class HubRequestForm(forms.ModelForm):

    class Meta:
        model = HubRequest
        fields = ('name', 'website', 'summary', 'description')
