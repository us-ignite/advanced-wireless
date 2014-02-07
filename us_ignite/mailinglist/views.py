import hashlib
import mailchimp

from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect
from django.template.response import TemplateResponse

from us_ignite.mailinglist.forms import EmailForm


def subscribe_email(email):
    master = mailchimp.Mailchimp(settings.MAILCHIMP_API_KEY)
    mailing_list = mailchimp.Lists(master)
    uid = hashlib.md5(email).hexdigest()
    email_data = {
        'email': email,
        'euid': uid,
        'leid': uid,
    }
    return mailing_list.subscribe(
        settings.MAILCHIMP_LIST, email_data)


def mailing_subscribe(request):
    """Handles MailChimp email registration."""
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            try:
                subscribe_email(form.cleaned_data['email'])
                messages.success(request, 'Successfully subscribed.')
                redirect_to = 'home'
            except mailchimp.ListAlreadySubscribedError:
                messages.error(request, 'Already subscribed.')
                redirect_to = 'mailing_subscribe'
            return redirect(redirect_to)
    else:
        form = EmailForm()
    context = {
        'form': form,
    }
    return TemplateResponse(request, 'mailinglist/form.html', context)
