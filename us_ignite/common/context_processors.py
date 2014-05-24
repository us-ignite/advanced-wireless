from django.conf import settings


def settings_available(request):
    return {
        'SITE_URL': settings.SITE_URL,
        'IS_PRODUCTION': settings.IS_PRODUCTION,
        'ACCOUNT_ACTIVATION_DAYS': settings.ACCOUNT_ACTIVATION_DAYS,
        'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID,
    }
