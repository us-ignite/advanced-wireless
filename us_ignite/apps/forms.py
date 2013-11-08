from django import forms

from us_ignite.apps.models import Application


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
        fields = ('name', 'description', 'assistance', 'technology',
                  'tags', 'status')
