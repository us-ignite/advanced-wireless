from nose.tools import eq_

from django.test import TestCase

from us_ignite.organizations.models import Organization
from us_ignite.organizations.tests import fixtures


class TestOrganizationActiveManager(TestCase):

    def tearDown(self):
        Organization.objects.all().delete()

    def test_published_organizations_are_returned(self):
        organization = fixtures.get_organization(status=Organization.PUBLISHED)
        eq_(list(Organization.active.all()), [organization])

    def test_unpublished_organizations_are_not_returned(self):
        organization = fixtures.get_organization(status=Organization.DRAFT)
        eq_(list(Organization.active.all()), [])
