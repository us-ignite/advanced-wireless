from nose.tools import eq_

from django.test import TestCase

from us_ignite.common.tests import utils
from us_ignite.common import context_processors


class TestSettingsAvailableContextProcessor(TestCase):

    def test_settings_are_available(self):
        request = utils.get_request('get', '/')
        context = context_processors.settings_available(request)
        eq_(sorted(context.keys()),
            sorted(['ACCOUNT_ACTIVATION_DAYS', 'GOOGLE_ANALYTICS_ID',
                    'IS_PRODUCTION', 'SITE_URL']))
