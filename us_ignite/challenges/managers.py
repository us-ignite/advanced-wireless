from collections import namedtuple

from django.db import models


AppEntry = namedtuple('AppEntry', ['application', 'entry'])


class ActiveChallengesManager(models.Manager):

    def get_query_set(self, *args, **kwargs):
        return (super(ActiveChallengesManager, self)
                .get_queryset(*args, **kwargs)
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

    def get_entries_for_apps(self, challenge, application_list):
        ids = [a.id for a in application_list]
        entries = self.get_query_set().filter(
            challenge=challenge, application__id__in=ids)
        entries_dict = {e.application_id: e for e in entries}
        result = []
        for app in application_list:
            entry = entries_dict.get(app.id, None)
            app_entry = AppEntry(application=app, entry=entry)
            result.append(app_entry)
        return result
