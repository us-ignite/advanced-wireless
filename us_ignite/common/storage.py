import logging

from django.conf import settings
from django.core.files.storage import get_storage_class

from storages.backends.s3boto import S3BotoStorage

logger = logging.getLogger('us_ignite.common.storage')


STATIC_LOCATION = 'static/%s' % settings.STATIC_FILES_VERSION


class StaticS3Storage(S3BotoStorage):

    def __init__(self, *args, **kwargs):
        super(StaticS3Storage, self).__init__(
            location=STATIC_LOCATION, *args, **kwargs)

    def url(self, name):
        url = super(StaticS3Storage, self).url(name)
        if name.endswith('/') and not url.endswith('/'):
            url += '/'
        return url


class MediaS3Storage(S3BotoStorage):

    def download_url(self, name):
        name = self._normalize_name(self._clean_name(name))
        return self.connection.generate_url(
            self.querystring_expire, method='GET',
            bucket=self.bucket.name, key=self._encode_name(name),
            query_auth=self.querystring_auth, force_http=True,
            response_headers={'response-content-disposition': 'attachment'})


class CachedS3BotoStorage(S3BotoStorage):
    """S3 storage backend that saves the files locally, too."""
    def __init__(self, location=STATIC_LOCATION, *args, **kwargs):
        super(CachedS3BotoStorage, self).__init__(
            location=location, *args, **kwargs)
        self.local_storage = get_storage_class(
            "compressor.storage.CompressorFileStorage")()

    def save(self, name, content):
        name = super(CachedS3BotoStorage, self).save(name, content)
        self.local_storage._save(name, content)
        return name
