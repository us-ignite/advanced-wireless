from collections import Counter

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.http import urlquote
from django.template.response import TemplateResponse

from us_ignite.apps.models import Application, Domain
from us_ignite.common.response import json_response


def _get_domain(label):
    domain = Domain.objects.get(name__exact=label)
    return domain.slug


URLS = {
    'stage': ('app_list_stage', Application.get_stage_id),
    'domain': ('app_list_domain', _get_domain)
}


def _get_search_url(name, label):
    if name in URLS:
        slug, function = URLS[name]
        args = [function(label)] if function else []
        path = reverse(slug, args=args)
    else:
        path = '%s?q=%s' % (reverse('search'), urlquote(label))
    return u'%s%s' % (settings.SITE_URL, path)


def get_chart_data(counter, name):
    chart_data = []
    for i, (key, value) in enumerate(counter.items()):
        chart_data.append({
            'label': key,
            'value': value,
            'id': '%s-%s' % (name, i),
            'url': _get_search_url(name, key),
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
        'domain': get_chart_data(Counter(domain_list), 'domain'),
        'stage': get_chart_data(Counter(stage_list), 'stage'),
        'feature': get_chart_data(Counter(feature_list), 'feature'),
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
