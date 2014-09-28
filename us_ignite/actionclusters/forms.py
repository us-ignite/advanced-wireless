from django import forms

from us_ignite.common import output
from us_ignite.apps.models import Feature
from us_ignite.actionclusters.models import ActionCluster, ActionClusterRequest


class ActionClusterRequestForm(forms.ModelForm):

    class Meta:
        model = ActionClusterRequest
        fields = ('name', 'website', 'summary', 'description')


class ActionClusterForm(forms.ModelForm):
    features = forms.ModelMultipleChoiceField(
        queryset=Feature.objects.all(), required=False,
        widget=forms.CheckboxSelectMultiple)

    def clean_tags(self):
        if 'tags' in self.cleaned_data:
            return output.prepare_tags(self.cleaned_data['tags'])

    class Meta:
        model = ActionCluster
        fields = ('name', 'website', 'summary', 'description', 'image',
                  'features', 'tags')


class ActionClusterAppMembershipForm(forms.Form):
    hubs = forms.ModelMultipleChoiceField(
        label=u'Communities',
        queryset=ActionCluster.objects.filter(status=ActionCluster.PUBLISHED),
        required=False, widget=forms.CheckboxSelectMultiple,
        help_text=u'Is the Application Connected to a US Ignite '
        'Community or Partner? (e.g. Funding, Development, Piloting, '
        'Testing, etc.)')


class ActionClusterApprovalRequestForm(forms.ModelForm):

    class Meta:
        model = ActionClusterRequest
        fields = ('status', 'notes')

