from django import forms
from django.forms.models import inlineformset_factory

from us_ignite.apps.models import Feature
from us_ignite.hubs.models import Hub, HubAppMembership, HubRequest


class HubRequestForm(forms.ModelForm):

    class Meta:
        model = HubRequest
        fields = ('name', 'website', 'summary', 'description')


class HubForm(forms.ModelForm):
    features = forms.ModelMultipleChoiceField(
        queryset=Feature.objects.all(), required=False,
        widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Hub
        fields = ('name', 'website', 'summary', 'description', 'image',
                  'features', 'tags')


class HubAppMembershipForm(forms.Form):
    hubs = forms.ModelMultipleChoiceField(
        queryset=Hub.objects.filter(status=Hub.PUBLISHED),
        required=False, widget=forms.CheckboxSelectMultiple)
