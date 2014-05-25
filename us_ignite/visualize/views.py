from collections import Counter

from us_ignite.common.response import json_response
from django.template.response import TemplateResponse

from us_ignite.apps.models import Application


def get_chart_data(counter):
    chart_data = []
    for key, value in counter.items():
        chart_data.append({
            'label': key,
            'value': value,
        })
    return chart_data


def get_app_stats():
    app_list = Application.objects.select_related('domain').all()
    domain_list = []
    stage_list = []
    feature_list = []
    for app in app_list:
        if app.domain:
            domain_list.append(app.domain.name)
        stage_list.append(app.get_stage_display())
        feature_list += [f.name for f in app.features.all()]
    stats = {
        'total': len(app_list),
        'domain': get_chart_data(Counter(domain_list)),
        'stage': get_chart_data(Counter(stage_list)),
        'feature': get_chart_data(Counter(feature_list)),
    }
    return stats

def get_hub_stats():
    stats = {}
    return stats


def visual_list(request):
    context = {
        'apps': get_app_stats(),
        'hubs': get_hub_stats(),
    }
    return TemplateResponse(request, 'visualize/object_list.html', context)


def visual_json(request):
    context = {
        'apps': get_app_stats(),
    }
    return json_response(context, callback='chart.render')
