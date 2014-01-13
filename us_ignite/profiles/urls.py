from django.conf.urls import patterns,  url
from django.contrib.auth.views import login

from us_ignite.common import decorators


urlpatterns = patterns(
    'us_ignite.profiles.views',
    url(r'^profile/$', 'user_profile', name='user_profile'),
    url(r'^profile/delete/$', 'user_profile_delete',
        name='user_profile_delete'),
    url(r'^register/$', 'registration_view', name='registration_register'),
    url(r'^activate/complete/$', 'registration_activation_complete',
        name='registration_activation_complete'),
    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]{40} because a bad activation key should still get to
    # the view; that way it can return a sensible "invalid key" message
    # instead of a confusing 404.
    url(r'^activate/(?P<activation_key>\w+)/$', 'registration_activate',
        name='registration_activate'),
    url(r'^register/complete/$', 'registration_complete',
        name='registration_complete'),
    url(r'^register/closed/$', 'registration_disallowed',
        name='registration_disallowed'),
)

urlpatterns += patterns(
    'django.contrib.auth.views',
    url(r'^login/$', decorators.not_auth_required(login),
        {'template_name': 'registration/login.html'}, name='auth_login'),
    url(r'^logout/$', 'logout',
        {'template_name': 'registration/logout.html'}, name='auth_logout'),
    url(r'^password/change/$', 'password_change', name='password_change'),
    url(r'^password/change/done/$', 'password_change_done',
        name='password_change_done'),
    url(r'^password/reset/$', 'password_reset', name='password_reset'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        'password_reset_confirm', name='password_reset_confirm'),
    url(r'^password/reset/complete/$', 'password_reset_complete',
        name='password_reset_complete'),
    url(r'^password/reset/done/$', 'password_reset_done',
        name='password_reset_done'),
)
