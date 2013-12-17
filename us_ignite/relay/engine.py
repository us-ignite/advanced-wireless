import logging


from django.core import mail
from django.conf import settings
from django.template.loader import render_to_string


logger = logging.getLogger('us_ignite.relay')


def contact_user(destinatary, reply_to, context):
    _template = lambda t: 'relay/%s.txt' % t
    subject = render_to_string(_template('subject'), context)
    subject = ''.join(subject.splitlines())
    body = render_to_string(_template('body'), context)
    email = mail.EmailMessage(
        subject, body, settings.DEFAULT_FROM_EMAIL, [destinatary],
        headers={'Reply-To': reply_to})
    return email.send()
