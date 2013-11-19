"""
https://djangosnippets.org/snippets/1868/
http://developer.amazonwebservices.com/connect/entry.jspa?externalID=1434

<input type="hidden" name="key" value="uploads/${filename}">
<input type="hidden" name="AWSAccessKeyId" value="YOUR_AWS_ACCESS_KEY">
<input type="hidden" name="acl" value="private">
<input type="hidden" name="success_action_redirect" value="http://localhost/">
<input type="hidden" name="policy" value="YOUR_POLICY_DOCUMENT_BASE64_ENCODED">
<input type="hidden" name="signature" value="YOUR_CALCULATED_SIGNATURE">
<input type="hidden" name="Content-Type" value="image/jpeg">
"""

import base64
import datetime
import hmac
import json

from hashlib import sha1

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe


class S3UploadForm(forms.Form):
    """Form to upload directly a file to S3.

    Usage:

    S3UploadForm(
        settings.AWS_ACCESS_KEY_ID,
        settings.AWS_SECRET_ACCESS_KEY,
        settings.AWS_STORAGE_BUCKET_NAME,
        key)

    Spec in:
    http://developer.amazonwebservices.com/connect/entry.jspa?externalID=1434
    """
    key = forms.CharField(widget=forms.HiddenInput)
    AWSAccessKeyId = forms.CharField(widget=forms.HiddenInput)
    acl = forms.CharField(widget=forms.HiddenInput)
    success_action_redirect = forms.CharField(widget=forms.HiddenInput)
    policy = forms.CharField(widget=forms.HiddenInput)
    signature = forms.CharField(widget=forms.HiddenInput)
    success_action_status = forms.CharField(widget=forms.HiddenInput)
    Content_Type = forms.CharField(widget=forms.HiddenInput)
    file = forms.FileField()

    def __init__(
            self, aws_access_key, aws_secret_key, bucket, key,
            expires_after=datetime.timedelta(hours=1),
            acl='public-read',
            success_action_redirect=None,
            content_type='',
            min_size=0,
            max_size=None
    ):
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key
        self.bucket = bucket
        self.key = key
        self.expires_after = expires_after
        self.acl = acl
        self.success_action_redirect = success_action_redirect
        self.content_type = content_type
        self.min_size = min_size
        self.max_size = max_size
        self.success_action_status = '201'
        policy = base64.b64encode(self.calculate_policy())
        signature = self.sign_policy(policy)
        initial = {
            'key': self.key,
            'AWSAccessKeyId': self.aws_access_key,
            'acl': self.acl,
            'policy': policy,
            'signature': signature,
            'success_action_status': self.success_action_status,
            'Content-Type': self.content_type,
        }
        if self.success_action_redirect:
            initial['success_action_redirect'] = self.success_action_redirect
        super(S3UploadForm, self).__init__(initial=initial)
        # Manually rename the Content_Type field to Content-Type:
        self.fields['Content-Type'] = self.fields['Content_Type']
        del self.fields['Content_Type']
        # Don't show success_action_redirect if it's not being used
        if not self.success_action_redirect:
            del self.fields['success_action_redirect']

    def as_html(self):
        """
        Use this instead of as_table etc, because S3 requires the file field
        come AFTER the hidden fields, but Django's normal form display methods
        position the visible fields BEFORE the hidden fields.
        """
        html = ''.join(map(unicode, self.hidden_fields()))
        html += unicode(self['file'])
        return html

    def as_form_html(self, prefix='', suffix=''):
        html = """
        <form action="%s" method="post" enctype="multipart/form-data">
        <p>%s <input type="submit" value="Upload"></p>
        </form>
        """.strip() % (self.action(), self.as_html())
        return mark_safe(html)

    def is_multipart(self):
        return True

    def action(self):
        return '//%s.s3.amazonaws.com/' % self.bucket

    def calculate_policy(self):
        conditions = [
            {'bucket': self.bucket},
            {'acl': self.acl},
            {'success_action_status': self.success_action_status},
            ['content-length-range', '2048', '%s' % self.max_size],
            ['starts-with', '$key', self.key.replace('${filename}', '')],
            ["starts-with", "$Content-Type", self.content_type],
        ]
        if self.success_action_redirect:
            conditions.append({
                'success_action_redirect': self.success_action_redirect,
            })

        policy_document = {
            "expiration": (
                datetime.datetime.now() + self.expires_after
            ).isoformat().split('.')[0] + 'Z',
            "conditions": conditions,
        }
        return json.dumps(policy_document, indent=2)

    def sign_policy(self, policy):
        return base64.b64encode(
            hmac.new(self.aws_secret_key, policy, sha1).digest()
        )


def get_s3_upload_form(key, redirect_to=None):
    """Generates a direct s3 upload form for the given ``key``."""
    return S3UploadForm(
        settings.AWS_ACCESS_KEY_ID,
        settings.AWS_SECRET_ACCESS_KEY,
        settings.AWS_STORAGE_BUCKET_NAME,
        key,
        success_action_redirect=redirect_to,
        max_size=settings.MAX_UPLOAD_SIZE,
    )
