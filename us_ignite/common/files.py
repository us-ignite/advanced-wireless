import logging

import requests
from StringIO import StringIO

from django.core import files
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

logger = logging.getLogger('us_ignite.common.files')


def import_file(url, key):
    """Imports a given a fileURL and returs a valid key, if the key exist
    assumes it's the same file."""
    if default_storage.exists(key):
        logger.debug('Ignoring existing file: %s', key)
        return key
    logger.debug('Downloading: %s',  url)
    response = requests.get(url)
    image_file = files.File(StringIO(response.content))
    return default_storage.save(key, ContentFile(image_file.read()))
