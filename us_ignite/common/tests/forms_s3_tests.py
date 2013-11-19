import json

from mock import patch
from nose.tools import ok_, eq_

from django.conf import settings
from django.test import TestCase

from us_ignite.common import forms_s3


class TestS3UploadForm(TestCase):

    def test_form_can_be_instantiated(self):
        form = forms_s3.S3UploadForm('access', 'secret', 'bucket', 'file-key')
        eq_(form.aws_access_key, 'access')
        eq_(form.aws_secret_key, 'secret')
        eq_(form.bucket, 'bucket')
        eq_(form.key, 'file-key')
        ok_(form.expires_after)
        eq_(form.acl, 'public-read')
        eq_(form.success_action_redirect, None)
        eq_(form.content_type, '')
        eq_(form.min_size, 0)
        eq_(form.max_size, None)
        eq_(form.success_action_status, '201')

    def test_form_fields_are_not_sensitive(self):
        form = forms_s3.S3UploadForm('access', 'secret', 'bucket', 'file-key')
        expected_fields = sorted(
            ['key', 'AWSAccessKeyId', 'acl', 'policy', 'signature',
             'success_action_status', 'Content-Type', 'file']
        )
        eq_(sorted(form.fields.keys()), expected_fields)

    def test_form_can_be_rendered_as_html(self):
        form = forms_s3.S3UploadForm('access', 'secret', 'bucket', 'file-key')
        field_list = ['key', 'AWSAccessKeyId', 'acl', 'policy', 'signature',
                      'success_action_status', 'Content-Type', 'file']
        output = form.as_html()
        for field in field_list:
            ok_(field in output)

    def test_form_can_be_completely_rendered(self):
        form = forms_s3.S3UploadForm('access', 'secret', 'bucket', 'file-key')
        field_list = ['key', 'AWSAccessKeyId', 'acl', 'policy', 'signature',
                      'success_action_status', 'Content-Type', 'file']
        output = form.as_form_html()
        for field in field_list:
            ok_(field in output)
        ok_('<form' in output)
        ok_('submit' in output)

    def test_form_is_marked_as_multipart(self):
        form = forms_s3.S3UploadForm('access', 'secret', 'bucket', 'file-key')
        eq_(form.is_multipart(), True)

    def test_form_action_is_valid(self):
        form = forms_s3.S3UploadForm('access', 'secret', 'bucket', 'file-key')
        eq_(form.action(), '//bucket.s3.amazonaws.com/')

    def test_calculate_policy_is_valid(self):
        form = forms_s3.S3UploadForm('access', 'secret', 'bucket', 'file-key')
        output = form.calculate_policy()
        json_output = json.loads(output)
        ok_('expiration' in json_output)
        eq_(json_output['conditions'],
            [
                {u'bucket': u'bucket'},
                {u'acl': u'public-read'},
                {u'success_action_status': u'201'},
                [u'content-length-range', u'2048', u'None'],
                [u'starts-with', u'$key', u'file-key'],
                [u'starts-with', u'$Content-Type', u'']
            ]
        )

    def test_calculate_policy_is_signed(self):
        form = forms_s3.S3UploadForm('access', 'secret', 'bucket', 'file-key')
        # Base64 of a SHA1 Calculated on a working version:
        eq_(form.sign_policy('foo'), 'm67ZG+f1i1fIJLYNp8smKy7K+9I=')


class TestGetS3UploadForm(TestCase):

    @patch('us_ignite.common.forms_s3.S3UploadForm')
    def test_form_can_be_instantiated(self, mock_form):
        forms_s3.get_s3_upload_form('my-key')
        mock_form.assert_called_once_with(
            settings.AWS_ACCESS_KEY_ID,
            settings.AWS_SECRET_ACCESS_KEY,
            settings.AWS_STORAGE_BUCKET_NAME,
            'my-key',
            success_action_redirect=None,
            max_size=settings.MAX_UPLOAD_SIZE,
        )
