import hashlib
import logging

from django.template.response import TemplateResponse
from forms import EmailForm
from forms import PawrEmailForm
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

    pawr_email_data = {
        'email': form_data['pawr_email'],
        'euid': uid,
        'leid': uid,
    }

    awt_merge_vars = {
        'FNAME': form_data['firstname'],
        'LNAME': form_data['lastname'],
        'ORGANIZATI': form_data['organization']
    }

    if form_data['email_list'] == 'default':
        return mailing_list.subscribe(settings.MAILCHIMP_PAWR_LIST, pawr_email_data)
    else:
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

    pawr_form = PawrEmailForm()
    context = {
        'form': form,
        'pawr_form': pawr_form
    }

    return TemplateResponse(request, 'awtmicrosite.html', context)


def awt_default_subscribe(request):
    if request.method == 'POST':
        pawr_form = PawrEmailForm(request.POST)
        if pawr_form.is_valid():
            try:
                subscribe_email(pawr_form.cleaned_data)
                messages.success(request, 'Successfully subscribed.')
                #redirect_to = 'awt_frontpage'
            except mailchimp.ListAlreadySubscribedError:
                messages.error(request, 'Already subscribed.')
                redirect_to = 'mailing_subscribe'
            except mailchimp.ValidationError, e:
                messages.error(request, 'ERROR: %s' % e.args[0])
                redirect_to = 'mailing_subscribe'
            return redirect(redirect_to)
    else:
        pawr_form = PawrEmailForm()

    form = EmailForm()
    context = {
        'form': form,
        'pawr_form': pawr_form
    }

    return TemplateResponse(request, 'awtmicrosite.html', context)
