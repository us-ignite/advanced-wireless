from django.conf.urls import url
from . import views


urlpatterns =[
    url(r'^$', views.actioncluster_list, {'current': True}, name='actioncluster_list'),
    url(r'^archive/$', views.actioncluster_list, {'current': False}, name='actioncluster_list_archive'),
    url(r'^needs-partner/$', views.actioncluster_list_partner,
        name='actioncluster_list_partner'),
    url(r'^iot-project-ideas/$', views.actioncluster_list_iot,
        name='actioncluster_list_iot'),
    url(r'^add/$', views.actioncluster_add, name='actioncluster_add'),

    url(r'^(?P<slug>[-\w]+)/$', views.actioncluster_detail,
        name='actioncluster_detail'),
    url(r'^(?P<slug>[-\w]+)/edit/$', views.actioncluster_edit,
        name='actioncluster_edit'),
    url(r'^(?P<slug>[-\w]+)/export/$', views.actioncluster_export,
        name='actioncluster_export'),
    url(r'^(?P<slug>[-\w]+)/hubs-membership/$', views.actioncluster_hub_membership,
        name='actioncluster_hub_membership'),
    url(r'^(?P<slug>[-\w]+)/membership/$', views.actioncluster_membership,
        name='actioncluster_membership'),
    url(r'^domain/(?P<domain>[-\w]+)/$', views.actioncluster_list,
        name='actioncluster_list_domain'),
    # url(r'^domain/(?P<domain>[-\w]+)/(?P<year>\d{4}/$', 'actioncluster_list',
    #     name='actioncluster_list_domain_by_year'),
    url(r'^stage/(?P<stage>[\d]{1})/$', views.actioncluster_list,
        name='actioncluster_list_stage'),
    url(r'^year/(?P<year>\d{4})/$', views.actioncluster_list,
        name='actioncluster_list_year'),
]
