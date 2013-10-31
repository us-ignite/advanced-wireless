import logging

from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

logger = logging.getLogger('us_ignite.profiles')


def send_welcome_email(user, **kwargs):
    """Sends a welcome email to the given ``User``"""
    if 'sender' in kwargs:
        logger.debug('Welcome email send via %s', kwargs['sender'])
    context = {
        'user': user,
    }
    _template = lambda t: 'profile/emails/welcome_%s.txt' % t
    subject = render_to_string(_template('subject'), context)
    subject = ''.join(subject.splitlines())
    body = render_to_string(_template('body'), context)
    return send_mail(
        subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])
