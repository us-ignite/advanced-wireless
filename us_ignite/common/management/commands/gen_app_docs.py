from collections import defaultdict

from django.core.management.base import BaseCommand
from django.contrib import admin
from django.contrib.auth.models import User
from django.test.client import RequestFactory


def _get_request(path='/admin/'):
    factory = RequestFactory()
    request = factory.get(path)
    # Dummy user required to avoid any ``admin`` validation.
    request.user = User(pk=1, is_superuser=True, is_staff=True)
    return request


def get_url(klass, suffix='/'):
    return u'/admin/%s/%s%s' % (
        klass._meta.app_label, klass._meta.object_name.lower(), suffix)


def underline_title(title, underline='-'):
    output = [title]
    output.append(underline * len(title))
    output += ['']
    return '\n'.join(output)


def get_note(text):
    return '\n'.join([
        '.. note::',
        '   %s' % text,
    ])


def get_image(klass, *args):
    suffix = '--'.join(args)
    suffix = ('--' + suffix) if suffix else suffix
    image_path = '../snapshots/admin--%s--%s%s.png' % (
        klass._meta.app_label, klass._meta.object_name.lower(), suffix)
    output = [
        '\n.. image:: %s' % image_path,
        '   :width: 100%',
    ]
    return '\n'.join(output)


def get_module_title(app):
    title = underline_title('%s admin section' % app, underline='=')
    output = [title]
    output += [
        'This section list the ``%s`` section and its usage in the site.' % app,
    ]
    return '\n'.join(output)


def get_app_title(klass, admin_form):
    return underline_title('Add %s' % klass._meta.object_name)


def get_app_list_description(klass, admin_form):
    url = get_url(klass, '/')
    title = klass._meta.verbose_name_plural.title()
    output = [
        underline_title('View existing %s' % title),
        ('The existing %s can be listed in the ``%s`` URL. From this '
         'section the details of these %s can be inspected.\n' % (title, url, title)),
        'And the following actions can be performed:\n',
    ]
    output.append('- View the details of the %s.' % title)
    if admin_form.list_filter:
        filters = ', '.join(admin_form.list_filter)
        output.append('- Filter the %s by: %s.' % (title, filters))
    if admin_form.search_fields:
        output.append('- Search the %s by their contents.' % title)
    output.append(get_image(klass))
    return '\n'.join(output)


def get_app_unpublishing_description(klass, admin_form):
    plural = klass._meta.verbose_name_plural.title()
    url = get_url(klass, '/')
    output = [
        underline_title('Unpublishing / Removing  %s' % plural),
        ('In case %s needs unpublishing it can be done from the detail'
         ' admin view by changing the ``status``'
         ' of the %s to ``draft`` or ``removed``\n' % (plural, plural)),
        get_note('The %s can be browsed in the ``%s`` URL.\n' % (plural, url)),
    ]
    return '\n'.join(output)


def get_field_list(klass, admin_form):
    request = _get_request()
    form_klass = admin_form.get_form(request)
    form = form_klass()
    plural = klass._meta.verbose_name_plural.title()
    output = ['\nThe following fields are available to create %s:\n' % plural]
    for key, field in form.fields.items():
        status = 'Required' if field.required else 'Optional'
        output.append('- %s: %s. %s' % (
            unicode(field.label), status, unicode(field.help_text)))
    return '\n'.join(output)


def get_app_add_description(klass, admin_form):
    plural = klass._meta.verbose_name_plural.title()
    url = get_url(klass, '/add/')
    output = [
        underline_title('Adding %s' % plural),
        'Adding %s can be done from the ``%s`` URL.' % (plural, url),
        get_field_list(klass, admin_form),
        '\nThese %s are created so ...' % plural,
        get_image(klass, 'add'),
    ]
    return '\n'.join(output)


def get_module_doc(label, item_list):
    output = [get_module_title(label)]
    for klass, admin_form in item_list:
        output += [
            get_app_list_description(klass, admin_form),
            get_app_add_description(klass, admin_form),
            get_app_unpublishing_description(klass, admin_form),
        ]
    return '\n\n\n'.join(output)


def get_filename(app):
    return u'admin_%s.rst' % app


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        try:
            module = args[0]
        except IndexError:
            module = None
        # Discover all t
        admin.autodiscover()
        registry = defaultdict(list)
        for klass, form in admin.site._registry.items():
            label = klass._meta.app_label
            registry[label].append((klass, form))
        for key, item_list in registry.items():
            output = get_module_doc(key, item_list)
            filename = get_filename(key)
            print 'Generating: %s' % filename
            with open(filename, 'w') as stream:
                stream.write(output)
        print 'Done'
