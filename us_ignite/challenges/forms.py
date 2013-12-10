from functools import partial

from django import forms

from us_ignite.challenges.models import Entry


question_field = partial(forms.CharField, widget=forms.Textarea)


def get_entry_choices():
    valid = [Entry.DRAFT, Entry.SUBMITTED]
    return [i for i in Entry.STATUS_CHOICES if i[0] in valid]


def get_field_name(question_id):
    return u'question_%s' % question_id


def get_challenge_form(challenge):
    """Generate a dynamic form from the ``Questions`` in a ``Challenge``

    The name of the field is a variation of the ``question.id``.
    """
    question_list = challenge.question_set.all()
    properties = {
        'status': forms.ChoiceField(choices=get_entry_choices()),
    }
    for question in question_list:
        name = get_field_name(question.id)
        properties[name] = question_field(
            label=question.question, required=question.is_required)
    return type('ChallengeForm', (forms.Form, ), properties)


def get_challenge_initial_data(entry):
    """Generates the entry initial data for the ``ChallengeForm``

    The data is bind to each dynamic field by the question id
    which is unique and replicable between challenges and entries."""
    answer_list = entry.entryanswer_set.all()
    initial_data = {
        'status': entry.status,
    }
    for answer in answer_list:
        name = get_field_name(answer.question_id)
        initial_data[name] = answer.answer
    return initial_data
