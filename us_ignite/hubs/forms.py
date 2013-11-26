from django import forms

from us_ignite.hubs.models import Hub


class HubForm(forms.ModelForm):

    class Meta:
        model = Hub
        fields = ('name', 'website', 'summary', 'description')
