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
        eq_(profile.user, user)
        ok_(profile.slug)
        eq_(profile.website, '')
        eq_(profile.bio, '')
        ok_(profile.created)
        ok_(profile.modified)
        eq_(list(profile.tags.all()), [])
        eq_(profile.is_public, False)
        ok_(profile.position)

    def test_user_full_name_is_valid(self):
        user = fixtures.get_user('john')
        profile = fixtures.get_profile(user=user, name='John Donne')
        eq_(profile.full_name, u'John Donne')

    def test_gravatar_url_exists(self):
        user = fixtures.get_user('paul')
        profile = fixtures.get_profile(user=user)
        eq_(profile.get_gravatar_url(),
            '//www.gravatar.com/avatar/f978b2b03ad48da6d36c431f72d6fd97?s=100')

    def test_user_display_name_is_valid(self):
        user = fixtures.get_user('john')
        profile = fixtures.get_profile(user=user, name='John Donne')
        eq_(profile.display_name, u'John Donne')

    def test_empty_profile_user_display_name_is_valid(self):
        user = fixtures.get_user('john')
        profile = fixtures.get_profile(user=user)
        eq_(profile.display_name, u'US Ignite user')

    def test_display_email(self):
        user = fixtures.get_user('john', email='info@us-ignite.org')
        profile = fixtures.get_profile(user=user, name='john')
        eq_(profile.display_email, u'john <info@us-ignite.org>')

    def test_get_contact_url(self):
        user = fixtures.get_user('john', email='info@us-ignite.org')
        profile = fixtures.get_profile(user=user, name='john', slug='john')
        eq_(profile.get_contact_url(), u'/contact/john/')


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
