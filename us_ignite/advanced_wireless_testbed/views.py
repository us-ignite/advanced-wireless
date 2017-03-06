import hashlib
import logging

from django.template.response import TemplateResponse
from forms import EmailForm, PawrEmailForm, PotentialProposerForm, CompanyForm, InterestedObserverForm
import mailchimp
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import messages

logger = logging.getLogger('us_ignite.advanced_wireless_testbed.views')


def subscribe_email(form_data):
    master = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)

    mailing_list = mailchimp.Lists(master)

    uid = hashlib.md5(form_data['email']).hexdigest()
    email_address = form_data['email']

    email_data = {
        'email': email_address,
        'euid': uid,
        'leid': uid,
    }

    if form_data['email_list'] == 'awt_potential_proposers':
        awt_merge_vars = {
            'FNAME': form_data['firstname'],
            'LNAME': form_data['lastname'],
        }
        return mailing_list.subscribe(settings.MAILCHIMP_AWT_POTENTIAL_PROPOSER_LIST, email_data, awt_merge_vars)
    elif form_data['email_list'] == 'awt_companies':
        awt_merge_vars = {
            'FNAME': form_data['firstname'],
            'LNAME': form_data['lastname'],
            'ORGANIZATI': form_data['organization']
        }
        return mailing_list.subscribe(settings.MAILCHIMP_AWT_COMPANY_LIST, email_data, awt_merge_vars)
    elif form_data['email_list'] == 'awt_interested_observers':
        return mailing_list.subscribe(settings.MAILCHIMP_AWT_INTERESTED_OBSERVERS_LIST, email_data)
    else:
        return


def awt_frontpage(request):
    context = {
        'form': EmailForm(),
        'pawr_form': PawrEmailForm(),
        'potential_proposer_form': PotentialProposerForm(),
        'company_form': CompanyForm,
        'interested_observers': InterestedObserverForm,
    }

    return TemplateResponse(request, 'awtmicrosite.html', context)


def awt_default_subscribe(request, form=None):
    if request.method == 'POST':
        if form == 'potential_proposers':
            form = PotentialProposerForm(request.POST)
        elif form == 'awt_companies':
            form = CompanyForm(request.POST)
        elif form == 'interested_observers':
            form = InterestedObserverForm(request.POST)
        if form.is_valid():
            try:
                subscribe_email(form.cleaned_data)
                messages.success(request, 'Successfully subscribed.')
                redirect_to = 'awt_frontpage'
            except mailchimp.ListAlreadySubscribedError:
                messages.error(request, 'Already subscribed.')
                redirect_to = 'awt_frontpage'
            except mailchimp.ValidationError, e:
                messages.error(request, 'ERROR: %s' % e.args[0])
                redirect_to = 'awt_frontpage'
            except Exception, e:
                messages.error(request, 'ERROR: %s' % e.args[0])
                redirect_to = 'awt_frontpage'
            return redirect(redirect_to)

    context = {
        'form': EmailForm(),
        'pawr_form': PawrEmailForm(),
        'potential_proposer_form': PotentialProposerForm(),
        'company_form': CompanyForm,
        'interested_observers': InterestedObserverForm,
    }

    return TemplateResponse(request, 'awtmicrosite.html', context)


