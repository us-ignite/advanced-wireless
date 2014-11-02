from django.db import models
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils import timezone

from django_extensions.db.fields import (
    AutoSlugField, CreationDateTimeField, ModificationDateTimeField)
from taggit.managers import TaggableManager

from us_ignite.constants import IMAGE_HELP_TEXT
from us_ignite.common.fields import URL_HELP_TEXT
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
    slug = AutoSlugField(populate_from='name', unique=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    start_datetime = models.DateTimeField(
        help_text=u'Start date in %s timezone.' % settings.TIME_ZONE)
    end_datetime = models.DateTimeField(
        help_text=u'End date in %s timezone.' % settings.TIME_ZONE)
    url = models.URLField(
        blank=True, help_text=URL_HELP_TEXT, verbose_name=u'URL')
    is_external = models.BooleanField(
        default=False, help_text=u'Determines if the challenge is to be '
        'held in a different Site.')
    summary = models.TextField()
    description = models.TextField()
    event_dates = models.TextField(
        blank=True, help_text=u'Important event dates.')
    acknowledgments = models.TextField(
        blank=True, help_text=u'Partners/Sponsors/Acknowledgements')
    image = models.ImageField(
        upload_to="challenge", blank=True, help_text=IMAGE_HELP_TEXT)
    organization = models.ForeignKey(
        'organizations.Organization', blank=True, null=True)
    hide_entries = models.BooleanField(
        default=False, help_text=u'When active entries are published only '
        'after the Challenge has finished.')
    user = models.ForeignKey(
        'auth.User', blank=True, null=True, on_delete=models.SET_NULL,
        help_text=u'User responsible for this Challenge.')
    tags = TaggableManager(blank=True)
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

    def get_absolute_url(self):
        return reverse('challenge_detail', args=[self.slug])

    def get_admin_url(self):
        return reverse('admin:challenges_challenge_change', args=[self.id])

    def is_published(self):
        return self.status == self.PUBLISHED

    def is_draft(self):
        return self.status == self.DRAFT

    def is_removed(self):
        return self.status == self.REMOVED

    def is_open(self):
        """Check if the challenge dates are open and it is published."""
        now = timezone.now()
        return ((self.start_datetime <= now)
                and (now <= self.end_datetime)
                and self.is_published())

    def has_finished(self):
        now = timezone.now()
        return self.end_datetime < now


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
    SUBMITTED = 1
    DRAFT = 2
    REMOVED = 3
    STATUS_CHOICES = (
        (DRAFT, 'Draft'),
        (SUBMITTED, 'Submitted'),
        (REMOVED, 'Removed'),
    )
    challenge = models.ForeignKey('challenges.Challenge')
    application = models.ForeignKey('apps.Application')
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    notes = models.TextField(blank=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    # managers:
    objects = managers.EntryManager()

    class Meta:
        unique_together = ('challenge', 'application')
        verbose_name_plural = 'entries'

    def __unicode__(self):
        return u'Entry to %s for %s' % (self.application, self.challenge)

    def get_absolute_url(self):
        return reverse('entry_detail',
                       args=[self.challenge.slug, self.application.slug])

    def get_edit_url(self):
        return reverse('challenge_entry',
                       args=[self.challenge.slug, self.application.slug])

    def is_draft(self):
        return self.status == self.DRAFT

    def is_submitted(self):
        return self.status == self.SUBMITTED

    def is_removed(self):
        return self.status == self.REMOVED

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

    def is_visible_by(self, user):
        """Determines if the entry is visible by the given user."""
        if self.is_submitted():
            return True
        return user.is_authenticated() and self.application.owner_id == user.id


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
