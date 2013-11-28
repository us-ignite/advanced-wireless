from django import forms

from us_ignite.hubs.models import Hub, HubRequest


class HubRequestForm(forms.ModelForm):

    class Meta:
        model = HubRequest
        fields = ('name', 'website', 'summary', 'description')


class HubForm(forms.ModelForm):

    class Meta:
        model = Hub
        fields = ('name', 'website', 'summary', 'description')
