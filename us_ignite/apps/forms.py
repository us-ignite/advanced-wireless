from django import forms
from django.forms.models import inlineformset_factory

from us_ignite.apps.models import Application, ApplicationURL


def _get_status_choices():
    """Returns a list of valid user status for the ``Application``"""
    available_status = [
        Application.PUBLISHED,
        Application.DRAFT,
        Application.PRIVATE,
    ]
    is_valid_status = lambda x: x[0] in available_status
    return filter(is_valid_status, Application.STATUS_CHOICES)


class ApplicationForm(forms.ModelForm):
    """Model form for the ``Application`` with whitelisted fields."""
    status = forms.ChoiceField(
        choices=_get_status_choices(), initial=Application.DRAFT)

    class Meta:
        model = Application
        fields = ('name', 'short_description', 'description', 'stage',
                  'assistance', 'technology', 'tags', 'status')


ApplicationLinkFormSet = inlineformset_factory(
    Application, ApplicationURL, max_num=3, extra=3)
