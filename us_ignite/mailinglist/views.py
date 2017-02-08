import hashlib
import logging
import mailchimp

from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from us_ignite.mailinglist.forms import EmailForm

logger = logging.getLogger('us_ignite.mailinglist.views')


MAILING_LISTS = {
    'default': settings.MAILCHIMP_LIST,
    'globalcityteams': settings.MAILCHIMP_GCTC_LIST,
    'sgc_launch': settings.MAILCHIMP_SGC_LIST,
}


def subscribe_email(form_data, slug):
    if not slug in MAILING_LISTS:
        raise mailchimp.ValidationError('Error while subscribing.')

    master = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)

    mailing_list = mailchimp.Lists(master)
    uid = hashlib.md5(form_data['email']).hexdigest()
    email_data = {
        'email': form_data['email'],
        'euid': uid,
        'leid': uid,
    }
    if slug == 'globalcityteams':
        return mailing_list.subscribe(settings.MAILCHIMP_GCTC_LIST, email_data)
    elif slug == 'sgc_launch':
        return mailing_list.subscribe(settings.MAILCHIMP_SGC_LIST, email_data)
    else:
        return mailing_list.subscribe(settings.MAILCHIMP_LIST, email_data)

def mailing_subscribe(request, slug='default'):
    print slug
    """Handles MailChimp email registration."""
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            try:
                subscribe_email(form.cleaned_data, slug)
                messages.success(request, 'Successfully subscribed.')
                if slug == 'globalcityteams':
                    redirect_to = 'https://www.us-ignite.org/globalcityteams/'
                elif slug == 'sgc_launch':
                    redirect_to = 'smart_gigabit_communities_reverse_pitch'
                else:
                    redirect_to = 'home'
            except mailchimp.ListAlreadySubscribedError:
                messages.error(request, 'Already subscribed.')
                redirect_to = 'mailing_subscribe'
            except mailchimp.ValidationError, e:
                messages.error(request, 'ERROR: %s' % e.args[0])
                redirect_to = 'mailing_subscribe'
            return redirect(redirect_to)
    else:
        form = EmailForm()
    context = {
        'form': form,
    }
    return TemplateResponse(request, 'mailinglist/form.html', context)
