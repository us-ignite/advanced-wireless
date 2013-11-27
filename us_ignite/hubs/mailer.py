from django.core.mail import mail_admins
from django.template.loader import render_to_string


def notify_request(hub_request):
    """Notify US ignite about a user submitted ``HubRequest``."""
    context = {
        'object', hub_request,
    }
    subject = render_to_string('hubs/email/request_subject.txt', context)
    subject = ''.join(subject.splitlines())
    message = render_to_string('hubs/email/request_message.txt', context)
    return mail_admins(subject, message, fail_silently=True)
