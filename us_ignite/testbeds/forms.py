from django import forms

from us_ignite.testbeds.models import Testbed, NetworkSpeed

EMPTY_LABEL = u'- Select one -'


def get_experimentation_choices():
    return [('', EMPTY_LABEL)] + list(Testbed.EXPERIMENTATION_CHOICES)


class TestbedFilterForm(forms.Form):
    network_speed = forms.ModelChoiceField(
        queryset=NetworkSpeed.objects.all(), required=False,
        empty_label=EMPTY_LABEL)
    experimentation = forms.ChoiceField(
        choices=get_experimentation_choices(), required=False)
    passes_homes = forms.IntegerField(required=False, min_value=0)
    passes_business = forms.IntegerField(required=False, min_value=0)
    passes_anchor = forms.IntegerField(required=False, min_value=0)

    def clean(self):
        """Make sure at least one of the values is selected."""
        if not any(self.cleaned_data.values()):
            raise forms.ValidationError(u'Select at least one of the fields.')
        return self.cleaned_data
