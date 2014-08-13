from django.conf import settings
from django.core import mail
from django.template.loader import render_to_string


def notify_request(hub_request):
    """Notify US ignite about a user submitted ``HubRequest``."""
    context = {
        'object': hub_request,
        'SITE_URL': settings.SITE_URL,
    }
    subject = render_to_string('hubs/email/request_subject.txt', context)
    subject = ''.join(subject.splitlines())
    message = render_to_string('hubs/email/request_message.txt', context)
    email = mail.EmailMessage(
        subject, message, settings.DEFAULT_FROM_EMAIL,
        settings.IGNITE_MANAGERS)
    return email.send()
