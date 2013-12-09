from django.db import models


from django_extensions.db.fields import (
    AutoSlugField, CreationDateTimeField, ModificationDateTimeField)


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

    class Meta:
        ordering = ('-created', )

    def __unicode__(self):
        return self.name


class Question(models.Model):
    challenge = models.ForeignKey('challenges.Challenge')
    question = models.TextField()
    is_required = models.BooleanField(default=True)
    order = models.IntegerField(default=0)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    class Meta:
        ordering = ('order', )

    def __unicode__(self):
        return self.question


class Entry(models.Model):
    PENDING = 1
    ACCEPTED = 2
    REJECTED = 3
    WINNER = 4
    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (REJECTED, 'Rejected'),
        (WINNER, 'Winner'),
    )
    challenge = models.ForeignKey('challenges.Challenge')
    application = models.ForeignKey('apps.Application')
    status = models.IntegerField(choices=STATUS_CHOICES, default=PENDING)
    notes = models.TextField(blank=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    class Meta:
        unique_together = ('challenge', 'application')

    def __unicode__(self):
        return u'Entry to %s for %s' % (self.application, self.challenge)
