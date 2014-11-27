import pytz

from django import forms
from django.conf import settings
from django.forms.models import inlineformset_factory
from django.utils import timezone

from us_ignite.common import output
from us_ignite.events.models import Audience, Event, EventURL
from us_ignite.hubs.models import Hub
from us_ignite.organizations.models import Organization


def _get_status_choices():
    """Returns a list of valid user status for the ``Event``"""
    available_status = [
        Event.PUBLISHED,
        Event.DRAFT,
    ]
    is_valid_status = lambda x: x[0] in available_status
    return filter(is_valid_status, Event.STATUS_CHOICES)


DATE_HELP_TEXT = 'Format: YYYY-MM-DD HH:MM'


def _transform_date(aware_date, tz):
    default_tz = timezone.get_default_timezone()
    naive_date = timezone.make_naive(aware_date, timezone=default_tz)
    return timezone.make_aware(naive_date, timezone=pytz.timezone(tz))


class EventForm(forms.ModelForm):
    start_datetime = forms.DateTimeField(
        input_formats=settings.DATETIME_INPUT_FORMATS, help_text=DATE_HELP_TEXT,
        label=u'Start Date/Time')
    end_datetime = forms.DateTimeField(
        input_formats=settings.DATETIME_INPUT_FORMATS, required=False,
        help_text=DATE_HELP_TEXT, label=u'End Date/Time')
    status = forms.ChoiceField(
        choices=_get_status_choices(), initial=Event.DRAFT)
    hubs = forms.ModelMultipleChoiceField(
        queryset=Hub.objects.filter(status=Hub.PUBLISHED),
        required=False, widget=forms.CheckboxSelectMultiple)
    contact = forms.ModelChoiceField(
        queryset=Organization.active.all(), required=False,
        label='Organization')
    audiences = forms.ModelMultipleChoiceField(
        queryset=Audience.objects.all(), required=False,
        widget=forms.CheckboxSelectMultiple)

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        if not self.fields['contact'].queryset:
            del self.fields['contact']

    def clean_tags(self):
        if 'tags' in self.cleaned_data:
            return output.prepare_tags(self.cleaned_data['tags'])

    def save(self, *args, **kwargs):
        instance = super(EventForm, self).save(*args, **kwargs)
        # Replace tz aware datetime with the instance timezone:
        instance.start_datetime = _transform_date(
            instance.start_datetime, instance.timezone)
        if instance.end_datetime:
            instance.end_datetime = _transform_date(
                instance.end_datetime, instance.timezone)
        instance.save()
        return instance

    class Meta:
        fields = (
            'name', 'status', 'description', 'website', 'tickets_url',
            'image', 'start_datetime', 'end_datetime', 'timezone',
            'event_type', 'audiences', 'audience_other', 'scope', 'address',
            'position', 'contact', 'hubs', 'tags', 'actionclusters'
        )
        model = Event


EventURLFormSet = inlineformset_factory(
    Event, EventURL, max_num=3, can_delete=False)
