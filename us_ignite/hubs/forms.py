from django import forms

from us_ignite.common import output
from us_ignite.apps.models import Feature
from us_ignite.hubs.models import Hub, HubRequest


class HubRequestForm(forms.ModelForm):

    class Meta:
        model = HubRequest
        fields = ('name', 'website', 'summary', 'description')


class HubForm(forms.ModelForm):
    features = forms.ModelMultipleChoiceField(
        queryset=Feature.objects.all(), required=False,
        widget=forms.CheckboxSelectMultiple)

    def clean_tags(self):
        if 'tags' in self.cleaned_data:
            return output.prepare_tags(self.cleaned_data['tags'])

    class Meta:
        model = Hub
        fields = ('name', 'website', 'summary', 'description', 'image',
                  'features', 'tags')


class HubAppMembershipForm(forms.Form):
    hubs = forms.ModelMultipleChoiceField(
        label=u'Communities',
        queryset=Hub.objects.filter(status=Hub.PUBLISHED),
        required=False, widget=forms.CheckboxSelectMultiple,
        help_text=u'Is the Application Connected to a US Ignite '
        'Community or Partner? (e.g. Funding, Development, Piloting, '
        'Testing, etc.)')


class HubApprovalRequestForm(forms.ModelForm):

    class Meta:
        model = HubRequest
        fields = ('status', 'notes')
