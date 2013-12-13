from django.db import models
from django.utils import timezone


class ActiveChallengesManager(models.Manager):

    def get_query_set(self, *args, **kwargs):
        return (super(ActiveChallengesManager, self)
                .get_query_set(*args, **kwargs)
                .filter(~models.Q(status=self.model.REMOVED)))


class QuestionManager(models.Manager):

    def get_from_keys(self, form_keys, *args, **kwargs):
        question_ids = [int(k.replace('question_', '')) for k in form_keys]
        return (self.get_query_set()
                .filter(id__in=question_ids, *args, **kwargs))


class EntryManager(models.Manager):

    def get_entry_or_none(self, challenge, application):
        try:
            entry = self.get(challenge=challenge, application=application)
        except self.model.DoesNotExist:
            entry = None
        return entry
