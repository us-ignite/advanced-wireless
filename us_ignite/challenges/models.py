from django.db import models


from django_extensions.db.fields import (
    AutoSlugField, CreationDateTimeField, ModificationDateTimeField)

from us_ignite.challenges import managers


class Challenge(models.Model):
    PUBLISHED = 1
    DRAFT = 2
    REMOVED = 3
    STATUS_CHOICES = (
        (PUBLISHED, 'Published'),
        (DRAFT, 'Draft'),
        (REMOVED, 'Removed'),
    )
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    summary = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to="challenge", blank=True)
    organization = models.ForeignKey(
        'organizations.Organization', blank=True, null=True)
    user = models.ForeignKey('auth.User')
    notes = models.TextField(blank=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    # managers:
    objects = models.Manager()
    active = managers.ActiveChallengesManager()

    class Meta:
        ordering = ('-created', )

    def __unicode__(self):
        return self.name

    def is_published(self):
        return self.status == self.PUBLISHED

    def is_draft(self):
        return self.status == self.DRAFT

    def is_removed(self):
        return self.status == self.REMOVED


class Question(models.Model):
    challenge = models.ForeignKey('challenges.Challenge')
    question = models.TextField()
    is_required = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    # managers:
    objects = managers.QuestionManager()

    class Meta:
        ordering = ('order', )

    def __unicode__(self):
        return self.question


class Entry(models.Model):
    DRAFT = 0
    SUBMITTED = 1
    ACCEPTED = 2
    REJECTED = 3
    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (SUBMITTED, 'Submitted'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
    )
    challenge = models.ForeignKey('challenges.Challenge')
    application = models.ForeignKey('apps.Application')
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    notes = models.TextField(blank=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    class Meta:
        unique_together = ('challenge', 'application')
        verbose_name_plural = 'entries'

    def __unicode__(self):
        return u'Entry to %s for %s' % (self.application, self.challenge)

    def is_draft(self):
        return self.status == self.DRAFT

    def is_submitted(self):
        return self.status == self.SUBMITTED

    def is_accepted(self):
        return self.status == self.ACCEPTED

    def is_rejected(self):
        return self.status == self.REJECTED

    def save_answers(self, answers_data):
        """Create or update the answers for this user."""
        question_list = Question.objects.get_from_keys(answers_data.keys())
        answer_list = []
        for question in question_list:
            answer_text = answers_data['question_%s' % question.id]
            answer = EntryAnswer.get_or_create_answer(
                self, question, answer_text)
            answer_list.append(answer)
        return answer_list


class EntryAnswer(models.Model):
    entry = models.ForeignKey('challenges.Entry')
    question = models.ForeignKey('challenges.Question')
    answer = models.TextField(blank=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    class Meta:
        unique_together = ('entry', 'question')
        ordering = ('question__order', )

    def __unicode__(self):
        return u"%s: %s" % (self.question.question, self.answer)

    @classmethod
    def get_or_create_answer(cls, entry, question, answer_text):
        answer, is_new = cls.objects.get_or_create(
            entry=entry, question=question)
        # Only update the answer when the text is different:
        if not answer.answer == answer_text:
            answer.answer = answer_text
            answer.save()
        return answer
