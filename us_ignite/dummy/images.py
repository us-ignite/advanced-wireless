import random

from StringIO import StringIO

from django.core.files import base, storage

from us_ignite.dummy.identicon import identicon


def random_image(filename):
    filename = 'dummy/%s' % filename
    image = identicon.render_identicon(
        random.randint(5 ** 5, 10 ** 10), random.randint(254, 400))
    tmp_file = StringIO()
    image.save(tmp_file, 'PNG')
    return storage.default_storage.save(
        filename, base.ContentFile(tmp_file.getvalue()))
