from django.conf.urls import patterns, url

urlpatterns = patterns(
    'us_ignite.blog.views',
    url(r'^$', 'post_list', name='blog_post_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<slug>[-\w]+)/$',
        'post_detail', name='blog_post_detail'),
)
