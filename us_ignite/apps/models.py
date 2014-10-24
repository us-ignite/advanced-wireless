import watson

from hashlib import md5

from django.core.urlresolvers import reverse
from django.db import models

from django_extensions.db.fields import (
    AutoSlugField, CreationDateTimeField, ModificationDateTimeField)
from geoposition.fields import GeopositionField
from taggit.managers import TaggableManager

from us_ignite.constants import IMAGE_HELP_TEXT
from us_ignite.common.fields import AutoUUIDField, URL_HELP_TEXT
from us_ignite.apps import managers, search


class Feature(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __unicode__(self):
        return self.name


class Domain(models.Model):
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name', unique=True)

    def __unicode__(self):
        return self.name


class ApplicationBase(models.Model):
    """Abstract model for ``Application`` and ``ApplicationVersion`` fields."""
    IDEA = 1
    PROTOTYPE = 2
    DEVELOPMENT = 3
    DEPLOYED = 4
    COMMERCIALIZED = 5
    STAGE_CHOICES = (
        (IDEA, u'Idea Complete'),
        (PROTOTYPE, u'Prototype Complete'),
        (DEVELOPMENT, u'In Development'),
        (DEPLOYED, u'Deployed'),
        (COMMERCIALIZED, u'Commercialized'),
    )
    name = models.CharField(max_length=255, verbose_name=u'application name')
    stage = models.IntegerField(
        choices=STAGE_CHOICES, default=IDEA,
        help_text=u'Please select the option that best reflects your '
        'current progress')
    website = models.URLField(max_length=500, blank=True, help_text=URL_HELP_TEXT)
    image = models.ImageField(
        blank=True, upload_to='apps', max_length=500,
        help_text=u'E.g. logo, screenshot, application diagram, photo of demo. %s'
        % IMAGE_HELP_TEXT)
    summary = models.TextField(
        blank=True, help_text=u'One sentence (tweet-length) pitch/summary of '
        'the application')
    impact_statement = models.TextField(
        blank=True, help_text=u'Who benefits and how in one paragraph or less')
    assistance = models.TextField(
        blank=True, help_text=u'Are you looking for additional help for this'
        ' project? (e.g. specific technical skills, subject matter experts, '
        'design help, partners for pilots, etc)')
    team_name = models.CharField(
        max_length=255, blank=True, help_text=u'Organization/Company name '
        'of developers')
    team_description = models.TextField(blank=True)
    acknowledgments = models.TextField(
        blank=True, help_text=u'Is their anyone you want to acknowledge '
        'for supporting this application?')
    notes = models.TextField(blank=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    class Meta:
        abstract = True

    def get_signature(self):
        """Generate an md5 signature from the model values."""
        fields = [self.name, self.stage, self.website, self.image,
                  self.summary, self.impact_statement,
                  self.assistance, self.team_description,
                  self.acknowledgments]
        value = ''.join(['%s' % a for a in fields])
        return md5(value).hexdigest()

    @classmethod
    def get_stage_id(self, name):
        for pk, stage in self.STAGE_CHOICES:
            if stage == name:
                return pk
        return None

    def compare_stage(self, stage):
        if self.stage > stage:
            return 'passed'
        if self.stage == stage:
            return 'active'
        if self.stage < stage:
            return 'innactive'
        return ''

    def get_stage_list(self):
        stages = []
        for key, name in self.STAGE_CHOICES:
            stages.append((name, self.compare_stage(key)))
        return stages


class Application(ApplicationBase):
    """``Applications``add core

    Any content related field that needs to be versioned must be
    added to the ``ApplicationBase``"""
    PUBLISHED = 1
    DRAFT = 2
    REMOVED = 3
    STATUS_CHOICES = (
        (PUBLISHED, 'Published'),
        (DRAFT, 'Draft'),
        (REMOVED, 'Removed'),
    )
    slug = AutoUUIDField(unique=True, editable=True)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    is_featured = models.BooleanField(default=False)
    owner = models.ForeignKey(
        'auth.User', related_name='ownership_set', blank=True, null=True,
        on_delete=models.SET_NULL)
    members = models.ManyToManyField(
        'auth.User', through='apps.ApplicationMembership',
        related_name='membership_set')
    features = models.ManyToManyField(
        'apps.Feature', blank=True, help_text='Check all that apply')
    features_other = models.CharField(blank=True, max_length=255)
    domain = models.ForeignKey(
        'apps.Domain', blank=True, null=True,
        help_text='What is the primary public benefit priority area '
        'served by this application?')
    awards = models.TextField(blank=True, help_text=u'Recognition or Awards')
    tags = TaggableManager(blank=True)
    position = GeopositionField(blank=True)
    is_homepage = models.BooleanField(
        default=False, verbose_name='Show in the homepage?',
        help_text=u'If marked this element will be shown in the homepage.')

    # managers:
    objects = models.Manager()
    active = managers.ApplicationActiveManager()
    published = managers.ApplicationPublishedManager()

    class Meta:
        ordering = ('-is_featured', '-created')

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Replace any previous homepage application when published:
        if self.is_homepage and self.is_public():
            self.__class__.objects.all().update(is_homepage=False)
        return super(Application, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('app_detail', args=[self.slug])

    def get_edit_url(self):
        return reverse('app_edit', args=[self.slug])

    def get_membership_url(self):
        return reverse('app_membership', args=[self.slug])

    def get_hub_membership_url(self):
        return reverse('app_hub_membership', args=[self.slug])

    def get_export_url(self):
        return reverse('app_export', args=[self.slug])

    def is_public(self):
        """Verify if the ``Application`` is accessible by anyone."""
        return self.status == self.PUBLISHED

    def is_draft(self):
        """Verify if the ``Application`` is a draft."""
        return self.status == self.DRAFT

    def is_owned_by(self, user):
        """Validates if the given user owns the ``Application``."""
        return user.is_authenticated() and user.id == self.owner_id

    def has_member(self, user):
        """Validates if the given user is a member of this ``Application``."""
        if self.is_owned_by(user):
            return True
        if user.is_authenticated() and self.members.filter(pk=user.id):
            return True
        return False

    def is_visible_by(self, user):
        """Validates if this app is acessible by the given ``User``."""
        return self.is_public() or self.has_member(user)

    def is_editable_by(self, user):
        """Determines if the given user can edit the ``Application``"""
        if user.is_authenticated():
            if ((self.owner == user)
                or self.applicationmembership_set.filter(
                    user=user, can_edit=True)):
                return True
        return False

    def get_summary(self):
        return self.summary


class ApplicationMembership(models.Model):
    user = models.ForeignKey('auth.User')
    application = models.ForeignKey('apps.Application')
    can_edit = models.BooleanField(default=False)
    created = CreationDateTimeField()

    class Meta:
        unique_together = ('user', 'application')

    def __unicode__(self):
        return (u'Membership: %s for %s'
                % (self.application.name, self.user.email))


class ApplicationURL(models.Model):
    application = models.ForeignKey('apps.Application')
    name = models.CharField(max_length=255, blank=True)
    url = models.URLField(
        max_length=500, verbose_name=u'URL', help_text=URL_HELP_TEXT)

    def __unicode__(self):
        return self.url


class ApplicationMedia(models.Model):
    application = models.ForeignKey('apps.Application')
    name = models.CharField(max_length=255, blank=True)
    image = models.ImageField(upload_to='apps', max_length=500, blank=True,
                              help_text=IMAGE_HELP_TEXT)
    url = models.URLField(
        blank=True, verbose_name=u'URL', help_text=URL_HELP_TEXT)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def __unicode__(self):
        return 'Media: %s' % self.name

    class Meta:
        ordering = ('created', )


class ApplicationVersion(ApplicationBase):
    """Version of the ``Application``."""
    application = models.ForeignKey('apps.Application')
    slug = AutoUUIDField(unique=True, editable=True)
    # managers:
    objects = managers.ApplicationVersionManager()

    def __unicode__(self):
        return u'Version %s of application' % self.application

    def get_absolute_url(self):
        return reverse(
            'app_version_detail', args=[self.application.slug, self.slug])


class Page(models.Model):
    """Group of applications listed in a ``Page``."""
    PUBLISHED = 1
    DRAFT = 2
    FEATURED = 3
    STATUS_CHOICES = (
        (FEATURED, 'Featured'),
        (PUBLISHED, 'Published'),
        (DRAFT, 'Draft'),
    )
    name = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='name')
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    description = models.TextField(blank=True)
    created = CreationDateTimeField()
    modified = ModificationDateTimeField()

    def save(self, *args, **kwargs):
        if self.status == self.FEATURED:
            # Move any ``FEATURED`` page to ``PUBLISHED``,
            # only a single FEATURED page can be shown:
            (self.__class__.objects.filter(status=self.FEATURED)
             .update(status=self.PUBLISHED))
        return super(Page, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    def is_featured(self):
        return self.status == self.FEATURED

    def get_absolute_url(self):
        if self.is_featured():
            return reverse('apps_featured')
        return reverse('apps_featured_archive', args=[self.slug])


class PageApplication(models.Model):
    page = models.ForeignKey('apps.Page')
    application = models.ForeignKey('apps.Application')
    order = models.IntegerField(default=0)

    class Meta:
        ordering = ('order', )

    def __unicode__(self):
        return u'%s for page %s' % (self.application, self.page)

# Search
watson.register(
    Application.published.all(),
    search.ApplicationSearchAdapter
)
