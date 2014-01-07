from nose.tools import eq_, ok_

from django.test import TestCase

from us_ignite.uploads.models import Image, Upload


class TestImageModel(TestCase):

    def tearDown(self):
        Image.objects.all().delete()

    def test_image_is_created_successfully(self):
        data = {
            'image': 'image.png',
        }
        instance = Image.objects.create(**data)
        ok_(instance.id)
        eq_(instance.title, '')
        eq_(instance.image, 'image.png')
        ok_(instance.created)
        ok_(instance.modified)


class TestUploadModel(TestCase):

    def tearDown(self):
        Upload.objects.all().delete()

    def test_upload_is_created_successfully(self):
        data = {
            'attachment': 'document.pdf',
        }
        instance = Upload.objects.create(**data)
        ok_(instance.id)
        eq_(instance.title, '')
        eq_(instance.attachment, 'document.pdf')
        ok_(instance.created)
        ok_(instance.modified)
