import logging

from collections import namedtuple

from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string

from django_browserid import auth
from us_ignite.profiles import models


logger = logging.getLogger('profiles.inviter')


RawUser = namedtuple('RawUser', ['name', 'email'])


def create_browserid_user(email, first_name=''):
    """Creates users the ``django_browserid`` way."""
    from django.db import IntegrityError
    username_algo = getattr(settings, 'BROWSERID_USERNAME_ALGO', None)
    if username_algo is not None:
        username = username_algo(email)
    else:
        username = auth.default_username_algo(email)
    try:
        return User.objects.create_user(username, email, first_name=first_name)
    except IntegrityError as err:
        # Race condition! Attempt to re-fetch from the database.
        logger.warning('IntegrityError during user creation: {0}'.format(err))
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        # Whatevs, let's re-raise the error.
        logger.exception(err)
        raise err


def create_user(raw_user):
    """Send an invitation to the user"""
    try:
        # Ignore existing users:
        User.objects.get(email=raw_user.email)
        return None
    except User.DoesNotExist:
        user = create_browserid_user(
            raw_user.email, first_name=raw_user.name)
    # Create a new profile:
    profile, new = models.Profile.objects.get_or_create(user=user)
    # Send profile invitation:
    return user


def send_user_invitation(raw_user):
    context = {
        'user': raw_user,
        'SITE_URL': settings.SITE_URL,
    }
    _template = lambda t: 'admin/profiles/invitation_%s' % t
    subject = render_to_string(_template('subject.txt'), context)
    subject = ''.join(subject.splitlines())
    body = render_to_string(_template('body.txt'), context)
    return send_mail(subject, body, settings.DEFAULT_FROM_EMAIL,
                     [raw_user.email])


def invite_users(row_list):
    user_list = []
    for row in row_list:
        raw_user = RawUser(*row)
        user = create_user(raw_user)
        if not user:
            # Ignore existing users.
            logger.debug('Ignoring existing account: %s <%s>',
                         raw_user.name, raw_user.email)
            continue
        user_list.append(user)
        send_user_invitation(raw_user)
    return user_list
