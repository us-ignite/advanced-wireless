from django.conf.urls import patterns, url

urlpatterns = patterns(
    'us_ignite.news.views',
    url(r'^$', 'article_list', name='article_list'),
)
