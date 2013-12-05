from django import forms
from django.conf import settings

from us_ignite.events.models import Event
from us_ignite.hubs.models import Hub


def _get_status_choices():
    """Returns a list of valid user status for the ``Application``"""
    available_status = [
        Event.PUBLISHED,
        Event.DRAFT,
    ]
    is_valid_status = lambda x: x[0] in available_status
    return filter(is_valid_status, Event.STATUS_CHOICES)


DATE_HELP_TEXT = 'Format: YYYY-MM-DD HH:MM'

class EventForm(forms.ModelForm):
    start_datetime = forms.DateTimeField(
        input_formats=settings.DATETIME_INPUT_FORMATS, help_text=DATE_HELP_TEXT)
    end_datetime = forms.DateTimeField(
        input_formats=settings.DATETIME_INPUT_FORMATS, required=False,
        help_text=DATE_HELP_TEXT)
    status = forms.ChoiceField(
        choices=_get_status_choices(), initial=Event.DRAFT)
    hubs = forms.ModelMultipleChoiceField(
        queryset=Hub.objects.filter(status=Hub.PUBLISHED),
        required=False, widget=forms.CheckboxSelectMultiple)

    class Meta:
        fields = (
            'name', 'status', 'website', 'image', 'start_datetime',
            'end_datetime', 'description', 'venue', 'position',
            'tags', 'hubs'
        )
        model = Event
