from nose.tools import eq_, ok_

from django.contrib.auth.models import User, AnonymousUser
from django.test import TestCase

from us_ignite.apps import models
from us_ignite.apps.tests import fixtures
from us_ignite.profiles.tests.fixtures import get_user


class TestApplicationModel(TestCase):

    def tearDown(self):
        for model in [User, models.Application]:
            model.objects.all().delete()

    def test_application_creation_is_successful(self):
        user = get_user('us-ignite')
        data = {
            'name': 'Gigabit app',
            'owner': user,
        }
        instance = models.Application.objects.create(**data)
        ok_(instance.id)
        eq_(instance.name, 'Gigabit app')
        ok_(instance.slug)
        eq_(instance.owner, user)
        eq_(instance.status, models.Application.DRAFT)
        eq_(instance.stage, models.Application.IDEA)
        eq_(instance.website, '')
        eq_(instance.image, '')
        eq_(instance.summary, '')
        eq_(instance.impact_statement, '')
        eq_(instance.description, '')
        eq_(instance.roadmap, '')
        eq_(instance.assistance, '')
        eq_(instance.team_description, '')
        eq_(instance.acknowledgments, '')
        eq_(instance.notes, '')
        ok_(instance.created)
        ok_(instance.modified)
        eq_(instance.is_featured, False)
        eq_(list(instance.features.all()), [])
        eq_(instance.domain, None)
        eq_(list(instance.members.all()), [])
        eq_(list(instance.tags.all()), [])

    def test_application_absolute_url(self):
        user = get_user('app-owner')
        application = fixtures.get_application(owner=user)
        eq_(application.get_absolute_url(), u'/apps/%s/' % application.slug)

    def test_application_edit_url(self):
        user = get_user('app-owner')
        application = fixtures.get_application(owner=user)
        eq_(application.get_edit_url(), u'/apps/%s/edit/' % application.slug)

    def test_membership_url(self):
        user = get_user('app-owner')
        application = fixtures.get_application(owner=user)
        eq_(application.get_membership_url(),
            u'/apps/%s/membership/' % application.slug)

    def test_hub_membership_url(self):
        user = get_user('app-owner')
        application = fixtures.get_application(owner=user)
        eq_(application.get_hub_membership_url(),
            u'/apps/%s/hubs-membership/' % application.slug)

    def test_application_version_url(self):
        user = get_user('app-owner')
        application = fixtures.get_application(owner=user)
        eq_(application.get_version_url(),
            u'/apps/%s/version/' % application.slug)

    def test_application_export_url(self):
        user = get_user('app-owner')
        application = fixtures.get_application(owner=user)
        eq_(application.get_export_url(),
            u'/apps/%s/export/' % application.slug)

    def test_application_is_public(self):
        user = get_user('app-owner')
        application = fixtures.get_application(
            owner=user, status=models.Application.PUBLISHED)
        ok_(application.is_public())

    def test_application_is_draft(self):
        user = get_user('app-owner')
        application = fixtures.get_application(
            owner=user, status=models.Application.DRAFT)
        ok_(application.is_draft())

    def test_application_ownership(self):
        user = get_user('app-owner')
        application = fixtures.get_application(owner=user)
        ok_(application.is_owned_by(user))

    def test_application_owner_membership(self):
        user = get_user('app-owner')
        application = fixtures.get_application(owner=user)
        ok_(application.has_member(user))

    def test_application_member_membership(self):
        user = get_user('app-owner')
        member = get_user('app-member')
        application = fixtures.get_application(owner=user)
        models.ApplicationMembership.objects.create(
            application=application, user=member)
        ok_(application.has_member(member))

    def test_published_app_is_visible_by_anon(self):
        user = get_user('app-owner')
        application = fixtures.get_application(
            owner=user, status=models.Application.PUBLISHED)
        ok_(application.is_visible_by(AnonymousUser()))

    def test_draft_app_is_visible_by_owner(self):
        user = get_user('app-owner')
        application = fixtures.get_application(
            owner=user, status=models.Application.DRAFT)
        ok_(application.is_visible_by(user))

    def test_draft_app_is_visible_by_member(self):
        user = get_user('app-owner')
        member = get_user('app-member')
        application = fixtures.get_application(
            owner=user, status=models.Application.DRAFT)
        models.ApplicationMembership.objects.create(
            application=application, user=member)
        ok_(application.is_visible_by(member))

    def test_app_is_editable_by_owner(self):
        user = get_user('app-owner')
        application = fixtures.get_application(
            owner=user, status=models.Application.DRAFT)
        ok_(application.is_editable_by(user))

    def test_app_is_editable_by_other_user(self):
        user = get_user('app-owner')
        member = get_user('app-member')
        application = fixtures.get_application(
            owner=user, status=models.Application.DRAFT)
        eq_(application.is_editable_by(member), False)

    def test_app_is_not_editable_by_anon(self):
        user = get_user('app-owner')
        application = fixtures.get_application(
            owner=user, status=models.Application.DRAFT)
        eq_(application.is_editable_by(AnonymousUser()), False)

    def test_app_is_editable_by_member_with_edit_permissions(self):
        user = get_user('app-owner')
        member = get_user('member')
        application = fixtures.get_application(
            owner=user, status=models.Application.DRAFT)
        models.ApplicationMembership.objects.create(
            application=application, user=member, can_edit=True)
        eq_(application.is_editable_by(member), True)

    def test_app_is_not_editable_by_member(self):
        user = get_user('app-owner')
        member = get_user('member')
        application = fixtures.get_application(
            owner=user, status=models.Application.DRAFT)
        models.ApplicationMembership.objects.create(
            application=application, user=member, can_edit=False)
        eq_(application.is_editable_by(member), False)

    def test_get_summary_shortens_description(self):
        user = get_user('app-owner')
        description = ' '.join(['word'] * 50)
        application = fixtures.get_application(
            owner=user, description=description)
        summary = application.get_summary()
        # 31 words considering the ellipsis:
        eq_(len(summary.split(' ')), 31)

    def test_get_summary_returns_existing_summary(self):
        user = get_user('app-owner')
        application = fixtures.get_application(
            owner=user, summary='summary', description='description')
        eq_(application.get_summary(), 'summary')

    def test_get_signature_is_generated(self):
        user = get_user('app-owner')
        application = fixtures.get_application(
            owner=user, summary='summary', description='description')
        ok_(application.get_signature())


class TestApplicationMembership(TestCase):

    def tearDown(self):
        for model in [User, models.Application, models.ApplicationMembership]:
            model.objects.all().delete()

    def test_application_membership_creation(self):
        user = get_user('app-owner')
        member = get_user('member')
        application = fixtures.get_application(owner=user)
        data = {
            'user': member,
            'application': application,
        }
        instance = models.ApplicationMembership.objects.create(**data)
        eq_(instance.user, member)
        eq_(instance.application, application)
        eq_(instance.can_edit, False)
        ok_(instance.created)


class TestApplicationURL(TestCase):

    def tearDown(self):
        for model in [User, models.Application, models.ApplicationURL]:
            model.objects.all().delete()

    def test_application_url_creation(self):
        user = get_user('app-owner')
        application = fixtures.get_application(owner=user)
        data = {
            'application': application,
            'url': 'http://us-ignite.org',
        }
        instance = models.ApplicationURL.objects.create(**data)
        ok_(instance.id)
        eq_(instance.application, application)
        eq_(instance.name, '')
        eq_(instance.url, 'http://us-ignite.org')


class TestApplicationVersionModel(TestCase):

    def tearDown(self):
        for model in [User, models.Application, models.ApplicationVersion]:
            model.objects.all().delete()

    def test_application_creation_is_successful(self):
        user = get_user('us-ignite')
        application = fixtures.get_application(
            name='Gigabit app', owner=user)
        data = {
            'application': application,
            'name': application.name,
        }
        instance = models.ApplicationVersion.objects.create(**data)
        ok_(instance.id)
        ok_(instance.application, application)
        eq_(instance.name, 'Gigabit app')
        eq_(instance.stage, models.Application.IDEA)
        eq_(instance.website, '')
        eq_(instance.image, '')
        ok_(instance.slug)
        ok_(instance.created)
        ok_(instance.modified)
        eq_(instance.summary, '')
        eq_(instance.impact_statement, '')
        eq_(instance.description, '')
        eq_(instance.roadmap, '')
        eq_(instance.assistance, '')
        eq_(instance.team_description, '')
        eq_(instance.acknowledgments, '')


class TestFeatureModel(TestCase):

    def tearDown(self):
        for model in [models.Feature]:
            model.objects.all().delete()

    def test_feature_creation_is_successful(self):
        instance = models.Feature.objects.create(**{
            'name': 'OpenFlow',
        })
        ok_(instance.id)
        eq_(instance.name, 'OpenFlow')
        ok_(instance.slug)


class TestPageModel(TestCase):

    def tearDown(self):
        for model in [models.Page]:
            model.objects.all().delete()

    def test_page_creation_is_successful(self):
        data = {
            'name': 'Featured apps',
        }
        instance = models.Page.objects.create(**data)
        ok_(instance.id)
        eq_(instance.name, 'Featured apps')
        ok_(instance.slug)
        eq_(instance.description, '')
        ok_(instance.created)
        ok_(instance.modified)
        eq_(instance.status, models.Page.DRAFT)

    def test_featured_page_is_swapped(self):
        fixtures.get_page(
            name='Awesome apps', status=models.Page.FEATURED)
        new_page = fixtures.get_page(
            name='Gigabit apps', status=models.Page.FEATURED)
        eq_(models.Page.objects.get(status=models.Page.FEATURED),
            new_page)

    def test_is_featured_property(self):
        page = fixtures.get_page(
            name='Awesome apps', status=models.Page.FEATURED)
        eq_(page.is_featured(), True)

    def test_get_absolute_url_featured(self):
        page = fixtures.get_page(
            name='Awesome apps', status=models.Page.FEATURED)
        eq_(page.get_absolute_url(), '/apps/featured/')

    def test_get_absolute_url_published(self):
        page = fixtures.get_page(
            name='older', status=models.Page.PUBLISHED)
        eq_(page.get_absolute_url(), '/apps/featured/archive/older/')


class TestPageApplication(TestCase):

    def tearDown(self):
        for model in [models.Application, models.Page]:
            model.objects.all().delete()

    def test_page_item_is_created_successfully(self):
        user = get_user('app-maker')
        application = fixtures.get_application(owner=user)
        page = fixtures.get_page(name='Awesome apps')
        data = {
            'application': application,
            'page': page,
        }
        instance = models.PageApplication.objects.create(**data)
        ok_(instance.id)
        eq_(instance.application, application)
        eq_(instance.page, page)
        eq_(instance.order, 0)
