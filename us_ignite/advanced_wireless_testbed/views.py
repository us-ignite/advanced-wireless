import hashlib
import logging

from django.template.response import TemplateResponse
from forms import EmailForm
import mailchimp
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages

logger = logging.getLogger('us_ignite.advanced_wireless_testbed.views')


def subscribe_email(form_data):

    master = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)

    mailing_list = mailchimp.Lists(master)
    uid = hashlib.md5(form_data['email']).hexdigest()
    email_data = {
        'email': form_data['email'],
        'euid': uid,
        'leid': uid,
    }
    awt_merge_vars = {
        'FNAME': form_data['firstname'],
        'LNAME': form_data['lastname'],
        'ORGANIZATI': form_data['organization']
    }
    return mailing_list.subscribe(settings.MAILCHIMP_AWT_LIST, email_data, awt_merge_vars)


def awt_frontpage(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            try:
                subscribe_email(form.cleaned_data)
                messages.success(request, 'Successfully subscribed.')
                redirect_to = 'awt_frontpage'
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
    return TemplateResponse(request, 'awtmicrosite.html', context)
