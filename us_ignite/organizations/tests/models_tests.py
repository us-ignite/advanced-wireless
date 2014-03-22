from nose.tools import eq_, ok_

from django.contrib.auth.models import User
from django.test import TestCase

from us_ignite.common.tests import utils
from us_ignite.profiles.tests.fixtures import get_user
from us_ignite.organizations.models import Organization, OrganizationMember
from us_ignite.organizations.tests import fixtures


class TestOrganization(TestCase):

    def tearDown(self):
        for model in [Organization, User]:
            model.objects.all().delete()

    def test_organization_can_be_created(self):
        data = {
            'name': 'US Ignite',
            'slug': 'us-ignite',
        }
        instance = Organization.objects.create(**data)
        ok_(instance.id)
        eq_(instance.name, 'US Ignite')
        eq_(instance.slug, 'us-ignite')
        eq_(instance.status, Organization.DRAFT)
        eq_(instance.bio, '')
        eq_(instance.image, '')
        eq_(instance.website, '')
        eq_(instance.interest_ignite, '')
        eq_(list(instance.interests.all()), [])
        eq_(instance.interests_other, '')
        eq_(instance.interest_ignite, '')
        eq_(instance.resources_available, '')
        eq_(list(instance.members.all()), [])
        eq_(list(instance.tags.all()), [])
        ok_(instance.created)
        ok_(instance.modified)
        ok_(instance.position)

    def test_organization_is_published(self):
        instance = fixtures.get_organization(status=Organization.PUBLISHED)
        eq_(instance.is_published(), True)

    def test_organization_is_draft(self):
        instance = fixtures.get_organization(status=Organization.DRAFT)
        eq_(instance.is_draft(), True)

    def test_organization_is_member(self):
        instance = fixtures.get_organization()
        user = get_user('member')
        OrganizationMember.objects.create(user=user, organization=instance)
        ok_(instance.is_member(user))

    def test_public_organization_is_visible(self):
        instance = fixtures.get_organization(status=Organization.PUBLISHED)
        eq_(instance.is_visible_by(utils.get_anon_mock()), True)

    def test_draft_organization_is_visible_by_member(self):
        instance = fixtures.get_organization(status=Organization.DRAFT)
        user = get_user('member')
        OrganizationMember.objects.create(user=user, organization=instance)
        eq_(instance.is_visible_by(user), True)

    def test_draft_organization_is_not_visible(self):
        instance = fixtures.get_organization(status=Organization.DRAFT)
        eq_(instance.is_visible_by(utils.get_anon_mock()), False)

    def test_get_absolute_url(self):
        instance = fixtures.get_organization(slug='ignite')
        eq_(instance.get_absolute_url(), '/org/ignite/')

    def test_get_edit_url(self):
        instance = fixtures.get_organization(slug='ignite')
        eq_(instance.get_edit_url(), '/org/ignite/edit/')
