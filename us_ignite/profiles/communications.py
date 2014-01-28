import logging

from django.core.mail import EmailMultiAlternatives, send_mail
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
    _template = lambda t: 'profile/emails/welcome_%s' % t
    subject = render_to_string(_template('subject.txt'), context)
    subject = ''.join(subject.splitlines())
    body = render_to_string(_template('body.txt'), context)
    body_html = render_to_string(_template('body.html'), context)
    email = EmailMultiAlternatives(
        subject, body, settings.DEFAULT_FROM_EMAIL, [user.email])
    email.attach_alternative(body_html, "text/html")
    return email.send()
