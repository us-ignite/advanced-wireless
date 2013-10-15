from django.conf import settings


def settings_available(request):
    return {
        'SITE_URL': settings.SITE_URL,
    }
