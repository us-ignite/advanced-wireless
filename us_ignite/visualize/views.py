from collections import Counter
from itertools import chain

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.http import urlquote
from django.template.response import TemplateResponse

from us_ignite.apps.models import Application, Domain
from us_ignite.actionclusters.models import ActionCluster, Domain as ACDomain
from us_ignite.common.response import json_response


def _get_domain(label):
    domain = Domain.objects.get(name__exact=label)
    return domain.slug

def _get_ac_domain(label):
    domain = ACDomain.objects.get(name__exact=label)
    return domain.slug

URLS = {
    'app_stage': ('app_list_stage', Application.get_stage_id),
    'app_domain': ('app_list_domain', _get_domain),
    'ac_stage': ('actioncluster_list_stage', ActionCluster.get_stage_id),
    'ac_domain': ('actioncluster_list_domain', _get_ac_domain)
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


def get_app_stats(display = 0):
    if display == 0:
        app_list = Application.objects.select_related('app_domain').all()
    else:
        app_list = Application.objects.select_related('app_domain').filter(status=display)
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
        'domain': get_chart_data(Counter(domain_list), 'app_domain'),
        'stage': get_chart_data(Counter(stage_list), 'app_stage'),
        'feature': get_chart_data(Counter(feature_list), 'feature'),
    }
    return stats

def get_actioncluster_stats(display = 0):
    if display == 0:
        ac_list = ActionCluster.objects.select_related('ac_domain').all()
    else:
        ac_list = ActionCluster.objects.select_related('ac_domain').filter(status=display)
    domain_list = []
    stage_list = []
    feature_list = []
    for ac in ac_list:
        if ac.domain:
            domain_list.append(ac.domain.name)
        stage_list.append(ac.get_stage_display())
        feature_list += [f.name for f in ac.features.all()]
    stats = {
        'total': len(ac_list),
        'domain': get_chart_data(Counter(domain_list), 'ac_domain'),
        'stage': get_chart_data(Counter(stage_list), 'ac_stage'),
        'feature': get_chart_data(Counter(feature_list), 'feature'),
    }
    return stats

def get_hub_stats():
    stats = {}
    return stats


def visual_list(request):
    context = {
        'apps': get_app_stats(1),
        'hubs': get_hub_stats(),
    }
    return TemplateResponse(request, 'visualize/object_list.html', context)


def visual_json(request):
    get_status = list(chain(get_app_stats(1), get_actioncluster_stats(1)))
    apps = get_app_stats(1)
    acs = get_actioncluster_stats(1)
    get_status = {
        'domain': list(chain(apps.get('domain'), acs.get('domain'))),
        'total': apps.get('total') + acs.get('total'),
        'feature': list(chain(apps.get('feature'), acs.get('feature'))),
        'stage': list(chain(apps.get('stage'), acs.get('stage')))
    }

    context = {
        'apps': get_app_stats(1),
        'ac': get_actioncluster_stats(1),
    }
    context = {
        'apps': get_status
    }

    return json_response(context, callback='chart.render')
