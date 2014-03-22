from django.test import TestCase
from django.contrib.auth.models import User

from django_nose.tools import assert_redirects
from registration.models import RegistrationProfile
from nose.tools import eq_

from us_ignite.common.tests import utils
from us_ignite.profiles.models import Profile, ProfileLink
from us_ignite.profiles.tests import fixtures


def _teardown_profiles():
    for model in [RegistrationProfile, Profile, User]:
        model.objects.all().delete()


class TestUnauthenticatedEditProfilePage(TestCase):

    def test_profile_requires_authentication(self):
        url = '/accounts/profile/'
        response = self.client.get(url)
        assert_redirects(response, utils.get_login_url(url))

    def test_profile_update_requires_authentication(self):
        url = '/accounts/profile/'
        data = {
            'name': 'John Donne',
        }
        response = self.client.post(url, data)
        assert_redirects(response, utils.get_login_url(url))


def _get_profilelink_inline_payload(profile_id, data_list=None, **kwargs):
    """Generates an inline form to be passed as part of the payload."""
    data_list = data_list if data_list else [{}]
    prefix = 'profilelink_set-'
    default = {
        '%sTOTAL_FORMS' % prefix: len(data_list),
        '%sINITIAL_FORMS' % prefix: 0,
        '%sMAX_NUM_FORMS'% prefix: 3,
    }
    for i, d in enumerate(data_list):
        default.update({
            '%s%s-name' % (prefix, i): d.get('name', ''),
            '%s%s-url' % (prefix, i): d.get('url', ''),
            '%s%s-DELETE' % (prefix, i): d.get('DELETE', ''),
            '%s%s-id' % (prefix, i): d.get('id', ''),
            '%s%s-profile' % (prefix, i): profile_id,
        })
    default.update(kwargs)
    return default


class TestEditProfilePage(TestCase):

    def setUp(self):
        self.user = fixtures.get_user('us-ignite', email='user@us-ignite.org')
        self.client.login(username='us-ignite', password='us-ignite')

    def tearDown(self):
        self.client.logout()
        _teardown_profiles()

    def test_profile_form_request_is_successful(self):
        url = '/accounts/profile/'
        response = self.client.get(url)
        fields = response.context['form'].fields.keys()
        eq_(sorted(fields),
            sorted(['bio', 'is_public', 'tags', 'website',
                    'position', 'availability', 'quote', 'interests_other',
                    'first_name', 'last_name', 'interests', 'skills', ]))

    def test_profile_form_update_is_successful(self):
        profile, is_new = Profile.objects.get_or_create(user=self.user)
        url = '/accounts/profile/'
        data = {
            'first_name': 'John',
            'last_name': 'Donne',
            'availability': Profile.NO_AVAILABILITY,
        }
        data.update(_get_profilelink_inline_payload(profile.pk))
        response = self.client.post(url, data)
        assert_redirects(response, '/accounts/profile/')
        profile = Profile.objects.get(user__username='us-ignite')
        eq_(profile.name, 'John Donne')
        eq_(profile.user.first_name, 'John')
        eq_(profile.user.last_name, 'Donne')

    def test_profile_ignores_invaid_values(self):
        profile, is_new = Profile.objects.get_or_create(user=self.user)
        url = '/accounts/profile/'
        data = {
            'email': 'invalid@us-ignite.org',
            'availability': Profile.NO_AVAILABILITY,
        }
        data.update(_get_profilelink_inline_payload(profile.pk))
        response = self.client.post(url, data)
        assert_redirects(response, '/accounts/profile/')
        values = (User.objects.values('email')
                  .get(username='us-ignite'))
        eq_(values, {'email': 'user@us-ignite.org'})

    def test_profile_updates_inline_models(self):
        profile, is_new = Profile.objects.get_or_create(user=self.user)
        url = '/accounts/profile/'
        data = {
            'name': '',
            'availability': Profile.NO_AVAILABILITY,
        }
        data_list = [{'name': 'Github', 'url': 'http://github.com/'}]
        data.update(_get_profilelink_inline_payload(
            profile.pk, data_list=data_list))
        response = self.client.post(url, data)
        assert_redirects(response, '/accounts/profile/')
        values = list(ProfileLink.objects.values('name', 'url')
                      .filter(profile=profile))
        eq_(values, [{'name': 'Github', 'url': 'http://github.com/'}])
