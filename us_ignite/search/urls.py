from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.search, name='search'),
    url(r'^apps/$', views.search_apps, name='search_apps'),
    url(r'^events/$', views.search_events, name='search_events'),
    url(r'^hubs/$', views.search_hubs, name='search_hubs'),
    url(r'^actionclusters/$', views.search_actionclusters, name='search_actionclusters'),
    url(r'^orgs/$', views.search_organizations, name='search_organizations'),
    url(r'^resources/$', views.search_resources, name='search_resources'),
    url(r'^tags.json$', views.tag_list, name='tag_list'),
]
