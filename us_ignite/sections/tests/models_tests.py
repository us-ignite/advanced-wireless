from nose.tools import eq_, ok_

from django.test import TestCase

from us_ignite.sections.models import Sponsor, SectionPage


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
        }
        instance = SectionPage.objects.create(**data)
        ok_(instance.id)
        eq_(instance.title, 'Custom page')
        eq_(instance.slug, 'custom-page')
        eq_(instance.body, '')
        eq_(instance.status, SectionPage.PUBLISHED)
        eq_(instance.template, '')
        ok_(instance.created)
