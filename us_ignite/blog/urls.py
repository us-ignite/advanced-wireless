from django.conf.urls import patterns, url

urlpatterns = patterns(
    'us_ignite.blog.views',
    url(r'^$', 'entry_list', name='blog_entry_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<slug>[-\w]+)/$',
        'entry_detail', name='blog_entry_detail'),
)
