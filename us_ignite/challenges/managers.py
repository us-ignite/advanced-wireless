from django.db import models
from django.utils import timezone


class ActiveChallengesManager(models.Manager):

    def get_query_set(self, *args, **kwargs):
        now = timezone.now()
        return (super(ActiveChallengesManager, self)
                .get_query_set(*args, **kwargs)
                .filter(start_datetime__lte=now,
                        end_datetime__gte=now, status=self.model.PUBLISHED))


class QuestionManager(models.Manager):

    def get_from_keys(self, form_keys, *args, **kwargs):
        question_ids = [int(k.replace('question_', '')) for k in form_keys]
        return (self.get_query_set()
                .filter(id__in=question_ids, *args, **kwargs))
