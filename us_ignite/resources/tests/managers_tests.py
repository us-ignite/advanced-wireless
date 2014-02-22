from nose.tools import eq_

from django.contrib.auth.models import User
from django.test import TestCase

from us_ignite.profiles.tests.fixtures import get_user
from us_ignite.resources.models import Resource
from us_ignite.resources.tests import fixtures


class TestResourcePublishedManager(TestCase):

    def tearDown(self):
        for model in [Resource, User]:
            model.objects.all().delete()

    def test_published_resources_are_returned(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(contact=user, status=Resource.PUBLISHED)
        eq_(list(Resource.published.all()), [resource])

    def test_unpublished_resources_are_not_returned(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(contact=user, status=Resource.DRAFT)
        eq_(list(Resource.published.all()), [])

    def test_featured_resource_is_returned(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(
            contact=user, status=Resource.PUBLISHED, is_featured=True)
        eq_(Resource.published.get_featured(), resource)

    def test_not_featured_resource_is_not_returned(self):
        user = get_user('us-ignite')
        resource = fixtures.get_resource(
            contact=user, status=Resource.PUBLISHED, is_featured=False)
        eq_(Resource.published.get_featured(), None)
