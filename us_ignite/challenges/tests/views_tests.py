from mock import Mock, patch
from nose.tools import assert_raises, eq_, ok_

from django.contrib.auth.models import User
from django.http import Http404
from django.test import TestCase

from us_ignite.common.tests import utils
from us_ignite.apps.models import Application
from us_ignite.apps.tests.fixtures import get_application
from us_ignite.challenges import views
from us_ignite.challenges.models import Challenge, Entry, EntryAnswer, Question
from us_ignite.challenges.tests import fixtures
from us_ignite.profiles.tests.fixtures import get_user


patch_filter = patch('us_ignite.challenges.models.Challenge.objects.filter')
patch_now = patch('django.utils.timezone.now')


class TestChallengeListView(TestCase):

    @patch_filter
    @patch_now
    def test_challenge_request_is_successful(self, mock_now, mock_filter):
        mock_now.return_value = 'now'
        request = utils.get_request('get', '/challenges/')
        response = views.challenge_list(request)
        eq_(response.status_code, 200)
        eq_(response.template_name, 'challenges/object_list.html')
        eq_(sorted(response.context_data.keys()), ['object_list'])
        mock_now.assert_called_once_with()
        mock_filter.assert_called_once_with(
            end_datetime__gte='now', status=Challenge.PUBLISHED)


class TestChallengeEntryView(TestCase):

    def _tear_down(self):
        for model in [Question, Entry, Challenge, Application, User]:
            model.objects.all().delete()

    def test_entry_request_requires_authentication(self):
        request = utils.get_request(
            'get', '/challenges/foo/enter/abc/', user=utils.get_anon_mock())
        response = views.challenge_entry(request, 'foo', 'abc')
        eq_(response.status_code, 302)
        eq_(response['Location'],
            utils.get_login_url('/challenges/foo/enter/abc/'))

    @patch('us_ignite.challenges.views.get_object_or_404')
    def test_challenge_does_not_exist(self, mock_get):
        mock_get.side_effect = Http404
        request = utils.get_request(
            'get', '/challenge/foo/enter/abc/', user=utils.get_user_mock())
        assert_raises(Http404, views.challenge_entry, request, 'foo', 'abc')
        mock_get.assert_called_once_with(Challenge.active, slug__exact='foo')

    @patch('us_ignite.challenges.views.get_object_or_404')
    def test_application_does_not_exist(self, mock_get):
        mock_get.side_effect = [Mock(spec=Challenge), Http404]
        request = utils.get_request(
            'get', '/challenges/foo/enter/abc/', user=utils.get_user_mock())
        assert_raises(Http404, views.challenge_entry, request, 'foo', 'abc')
        mock_get.assert_any_call(
            Application.active, slug__exact='abc', owner=request.user,
            status=Application.PUBLISHED)

    def test_challenge_form_is_returned_successful(self):
        user = get_user('us-ignite')
        challenge = fixtures.get_challenge(
            user=user, status=Challenge.PUBLISHED)
        app = get_application(owner=user, status=Application.PUBLISHED)
        question = fixtures.get_question(challenge)
        entry = fixtures.get_entry(app)
        EntryAnswer.get_or_create_answer(
            entry, question, 'Uses Gigabit features.')
        request = utils.get_request(
            'get', '/challenges/foo/enter/abc/', user=user)
        response = views.challenge_entry(
            request, challenge.slug, app.slug)
        eq_(response.status_code, 200)
        eq_(sorted(response.context_data.keys()),
            sorted(['form', 'challenge', 'application', 'entry']))
        context = response.context_data
        eq_(context['challenge'], challenge)
        eq_(context['application'], app)
        eq_(context['entry'], None)
        eq_(sorted(context['form'].fields.keys()),
            sorted(['question_%s' % question.id, 'status']))
        self._tear_down()

    def test_invalid_payload_fails(self):
        user = get_user('us-ignite')
        challenge = fixtures.get_challenge(
            user=user, status=Challenge.PUBLISHED)
        app = get_application(owner=user, status=Application.PUBLISHED)
        question = fixtures.get_question(challenge)
        entry = fixtures.get_entry(app)
        EntryAnswer.get_or_create_answer(
            entry, question, 'Uses Gigabit features.')
        request = utils.get_request(
            'post', '/challenges/foo/enter/abc/', data={}, user=user)
        response = views.challenge_entry(
            request, challenge.slug, app.slug)
        eq_(response.status_code, 200)
        eq_(sorted(response.context_data.keys()),
            sorted(['form', 'challenge', 'application', 'entry']))
        context = response.context_data
        eq_(context['challenge'], challenge)
        eq_(context['application'], app)
        ok_(context['entry'])
        eq_(sorted(context['form'].fields.keys()),
            sorted(['question_%s' % question.id, 'status']))
        ok_(context['form'].errors)
        self._tear_down()

    def test_valid_payload_succeeds(self):
        user = get_user('us-ignite')
        challenge = fixtures.get_challenge(
            user=user, status=Challenge.PUBLISHED)
        app = get_application(owner=user, status=Application.PUBLISHED)
        question = fixtures.get_question(challenge)
        entry = fixtures.get_entry(app)
        EntryAnswer.get_or_create_answer(
            entry, question, 'Uses Gigabit features.')
        question_id = 'question_%s' % question.id
        data = {
            'status': Entry.SUBMITTED,
            question_id: 'Answer for the question!'
        }
        url = '/challenges/%s/enter/%s/' % (challenge.slug, app.slug)
        request = utils.get_request('post', url, data=data, user=user)
        request._messages = utils.TestMessagesBackend(request)
        response = views.challenge_entry(
            request, challenge.slug, app.slug)
        eq_(response.status_code, 302)
        eq_(response['location'], url)
        entry = Entry.objects.get_entry_or_none(challenge, app)
        values = entry.entryanswer_set.values('answer', 'question_id').all()
        expected = [{
            'answer': 'Answer for the question!',
            'question_id': question.id
        }]
        eq_(list(values), expected)


patch_app_filter = patch('us_ignite.apps.models.Application.objects.filter')
patch_entry_filter = patch('us_ignite.challenges.models.Entry.objects'
                           '.get_entries_for_apps')


class TestChallengeDetailView(TestCase):

    @patch('us_ignite.challenges.views.get_object_or_404')
    def invalid_challenge_raises_404(self, mock_get):
        mock_get.side_effect = Http404
        request = utils.get_request(
            'get', '/challenges/gigabit/', user=utils.get_anon_mock())
        assert_raises(Http404, views.challenge_detail, request, 'gigabit')

    @patch_app_filter
    def challenge_detail_anon_request_is_valid(self, mock_filter):
        request = utils.get_request(
            'get', '/challenges/gigabit/', user=utils.get_anon_mock())
        response = views.challenge_detail(request, 'gigabit')
        eq_(response.status_code, 200)
        eq_(response.template_name, 'challenges/object_detail.html')
        eq_(sorted(response.context_data.keys()), ['entry_list', 'object'])
        eq_(mock_filter.call_count, 0)

    @patch_entry_filter
    @patch_app_filter
    @patch('us_ignite.challenges.views.get_object_or_404')
    def challenge_detail_auth_user_is_valid(self, mock_get, mock_app, mock_entry):
        mock_challenge = Mock(spec=Challenge)()
        mock_get.return_value = mock_challenge
        mock_app.return_value = ['app']
        request = utils.get_request(
            'get', '/challenges/gigabit/', user=utils.get_user_mock())
        response = views.challenge_detail(request, 'gigabit')
        eq_(response.status_code, 200)
        eq_(response.template_name, 'challenges/object_detail.html')
        eq_(sorted(response.context_data.keys()), ['entry_list', 'object'])
        mock_get.assert_called_once_with(
            Challenge.active, slug__exact='gigabit', status=Challenge.PUBLISHED)
        mock_app.assert_called_once_with(
            owner=request.user, status=Application.PUBLISHED)
        mock_entry.assert_called_once_with(mock_challenge, ['app'])


class TestEntryDetailView(TestCase):

    def test_entry_detail_requires_authentication(self):
        request = utils.get_request(
            'get', '/challenges/gigabit/app/', user=utils.get_anon_mock())
        response = views.entry_detail(request, 'gigabit', 'app')
        eq_(response.status_code, 302)
        eq_(response['Location'],
            utils.get_login_url('/challenges/gigabit/app/'))

    @patch('us_ignite.challenges.models.Entry.objects.select_related')
    def test_invalid_entry_raises_404(self, mock_get):
        mock_get.side_effect = Entry.DoesNotExist
        request = utils.get_request(
            'get', '/challenges/gigabit/app/', user=utils.get_user_mock())
        assert_raises(Http404, views.entry_detail, request, 'gigabit', 'app')

    @patch('us_ignite.challenges.models.Entry.objects.select_related')
    def test_not_published_entry_raises_404(self, mock_related):
        mock_related = mock_related.return_value
        mock_entry = Mock(spec=Entry)()
        mock_entry.is_visible_by.return_value = False
        mock_related.get.return_value = mock_entry
        request = utils.get_request(
            'get', '/challenges/gigabit/app/', user=utils.get_user_mock())
        assert_raises(Http404, views.entry_detail, request, 'gigabit', 'app')
        mock_entry.is_visible_by.assert_called_once_with(request.user)

    @patch('us_ignite.challenges.models.Entry.objects.select_related')
    def test_entry_request_is_successful(self, mock_related):
        mock_related = mock_related.return_value
        mock_entry = Mock(spec=Entry)()
        mock_entry.is_visible_by.return_value = True
        mock_related.get.return_value = mock_entry
        request = utils.get_request(
            'get', '/challenges/gigabit/app/', user=utils.get_user_mock())
        response = views.entry_detail(request, 'gigabit', 'app')
        eq_(response.status_code, 200)
        eq_(response.template_name, 'challenges/entry_detail.html')
        eq_(sorted(response.context_data.keys()),
            sorted(['challenge', 'application', 'entry',
                    'answer_list', 'is_owner'])
        )
        mock_entry.is_visible_by.assert_called_once_with(request.user)

    @patch('us_ignite.challenges.models.Entry.objects.select_related')
    def test_entry_is_visible_when_challenge_finishes(self, mock_related):
        mock_related = mock_related.return_value
        mock_entry = Mock(spec=Entry)()
        mock_entry.is_visible_by.return_value = True
        mock_entry.challenge.has_finished.return_value = True
        mock_related.get.return_value = mock_entry
        request = utils.get_request(
            'get', '/challenges/gigabit/app/', user=utils.get_user_mock())
        response = views.entry_detail(request, 'gigabit', 'app')
        eq_(response.status_code, 200)
        eq_(response.template_name, 'challenges/entry_detail.html')
        mock_entry.challenge.has_finished.assert_called_once()

    @patch('us_ignite.challenges.models.Entry.objects.select_related')
    def test_entry_is_visible_to_owner(self, mock_related):
        mock_related = mock_related.return_value
        mock_entry = Mock(spec=Entry)()
        mock_entry.is_visible_by.return_value = True
        mock_entry.application.is_owned_by.return_value = True
        mock_entry.challenge.has_finished.return_value = False
        mock_entry.challenge.hide_entries = True
        mock_related.get.return_value = mock_entry
        request = utils.get_request(
            'get', '/challenges/gigabit/app/', user=utils.get_user_mock())
        response = views.entry_detail(request, 'gigabit', 'app')
        eq_(response.status_code, 200)
        eq_(response.template_name, 'challenges/entry_detail.html')
        mock_entry.challenge.has_finished.assert_called_once()

    @patch('us_ignite.challenges.models.Entry.objects.select_related')
    def test_entry_is_not_visible_to_user_when_hidden(self, mock_related):
        mock_related = mock_related.return_value
        mock_entry = Mock(spec=Entry)()
        mock_entry.is_visible_by.return_value = True
        mock_entry.application.is_owned_by.return_value = False
        mock_entry.challenge.has_finished.return_value = False
        mock_entry.challenge.hide_entries = True
        mock_related.get.return_value = mock_entry
        request = utils.get_request(
            'get', '/challenges/gigabit/app/', user=utils.get_user_mock())
        assert_raises(Http404, views.entry_detail, request, 'gigabit', 'app')
        mock_entry.challenge.has_finished.assert_called_once()


class TestEntryWithdrawView(TestCase):

    def test_get_request_is_invalid(self):
        request = utils.get_request(
            'get', '/challenge/withdraw/4/', user=utils.get_user_mock())
        response = views.entry_withdraw(request, 4)
        eq_(response.status_code, 405)

    def test_request_requires_login(self):
        user = utils.get_anon_mock()
        request = utils.get_request(
            'post', '/challenge/withdraw/4/', data={}, user=user)
        response = views.entry_withdraw(request, 4)
        eq_(response.status_code, 302)
        eq_(response['Location'],
            utils.get_login_url('/challenge/withdraw/4/'))

    @patch('us_ignite.challenges.views.get_object_or_404')
    def test_withdraw_request_is_successful(self, mock_get):
        mock_entry = Mock(spec=Entry)()
        mock_entry.get_edit_url.return_value = u'/challenge/foo/app/'
        mock_get.return_value = mock_entry
        user = utils.get_user_mock()
        request = utils.get_request(
            'post', '/challenge/withdraw/4/', data={}, user=user)
        request._messages = utils.TestMessagesBackend(request)
        response = views.entry_withdraw(request, 4)
        eq_(response.status_code, 302)
        eq_(response['Location'], '/challenge/foo/app/')
        mock_entry.save.assert_called_once_with()
        mock_get.assert_called_once_with(
            Entry, pk=4, application__owner=request.user)
