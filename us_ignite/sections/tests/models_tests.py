from nose.tools import eq_, ok_

from django.test import TestCase

from us_ignite.common.tests import utils
from us_ignite.sections.models import Sponsor, SectionPage
from us_ignite.sections.tests import fixtures


class TestSponsorModel(TestCase):

    def tearDown(self):
        Sponsor.objects.all().delete()

    def test_instance_is_created_successfully(self):
        data = {
            'name': 'Mozilla',
            'image': 'logo.png',
            'website': 'http://mozilla.org',
        }
        instance = Sponsor.objects.create(**data)
        ok_(instance.id)
        eq_(instance.name, 'Mozilla')
        eq_(instance.website, 'http://mozilla.org')
        eq_(instance.image, 'logo.png')
        eq_(instance.order, 0)


class TestSectionPage(TestCase):

    def test_section_page_is_created_successfully(self):
        data = {
            'title': 'Custom page',
            'section': 'about',
        }
        instance = SectionPage.objects.create(**data)
        ok_(instance.id)
        eq_(instance.title, 'Custom page')
        eq_(instance.slug, 'custom-page')
        eq_(instance.section, 'about')
        eq_(instance.body, '')
        eq_(instance.status, SectionPage.PUBLISHED)
        eq_(instance.template, '')
        ok_(instance.created)

    def test_section_page_is_published(self):
        instance = fixtures.get_section_page(status=SectionPage.PUBLISHED)
        eq_(instance.is_published(), True)

    def test_section_page_is_visible_when_published(self):
        instance = fixtures.get_section_page(status=SectionPage.PUBLISHED)
        user = utils.get_anon_mock()
        ok_(instance.is_visible_by(user))

    def test_section_page_is_not_visible_when_not_published(self):
        instance = fixtures.get_section_page(status=SectionPage.DRAFT)
        user = utils.get_anon_mock()
        eq_(instance.is_visible_by(user), False)

    def test_non_published_page_is_visible_by_superuser(self):
        instance = fixtures.get_section_page(status=SectionPage.DRAFT)
        user = utils.get_user_mock()
        user.is_superuser = True
        ok_(instance.is_visible_by(user))

    def test_get_absolute_url(self):
        instance = fixtures.get_section_page(title='Custom title')
        eq_(instance.get_absolute_url(), '/about/custom-title/')
