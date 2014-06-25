from us_ignite.apps.models import Application


def applications_context(request):
    app_stages= []
    for pk, name in Application.STAGE_CHOICES:
        app_stages.append({'id': pk, 'name': name})
    return {
        'APP_STAGES': app_stages
    }
