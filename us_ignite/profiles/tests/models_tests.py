from nose.tools import ok_, eq_

from django.contrib.auth.models import User
from django.test import TestCase

from us_ignite.profiles.tests import fixtures
from us_ignite.profiles.models import Profile, ProfileLink


class TestProfileModel(TestCase):

    def tearDown(self):
        for model in [Profile, User]:
            model.objects.all().delete()

    def test_create_basic_profile_is_successful(self):
        user = fixtures.get_user('john')
        data = {
            'user': user,
        }
        profile = Profile.objects.create(**data)
        ok_(profile.pk)


class TestProfileLinkModel(TestCase):

    def tearDown(self):
        for model in [ProfileLink, Profile, User]:
            model.objects.all().delete()

    def test_create_basic_link_is_successful(self):
        user = fixtures.get_user('foo')
        profile = fixtures.get_profile(user=user)
        data = {
            'profile': profile,
            'url': 'http://us-ignite.org/',
        }
        link = ProfileLink.objects.create(**data)
        ok_(link.id)

    def test_profile_link_absolute_is_external_url(self):
        user = fixtures.get_user('foo')
        profile = fixtures.get_profile(user=user)
        data = {
            'profile': profile,
            'url': 'http://us-ignite.org/b/',
        }
        link = ProfileLink.objects.create(**data)
        eq_(link.url, 'http://us-ignite.org/b/')
