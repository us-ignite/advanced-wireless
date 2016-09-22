from django.conf.urls import url
from django.contrib.auth import views as auth

from us_ignite.common import decorators
from . import views

urlpatterns = [
    url(r'^profile/$', views.user_profile, name='user_profile'),
    url(r'^profile/delete/$', views.user_profile_delete,
        name='user_profile_delete'),
    url(r'^register/$', views.registration_view, name='registration_register'),
    url(r'^activate/complete/$', views.registration_activation_complete,
        name='registration_activation_complete'),
    # Activation keys get matched by \w+ instead of the more specific
    # [a-fA-F0-9]{40} because a bad activation key should still get to
    # the view; that way it can return a sensible "invalid key" message
    # instead of a confusing 404.
    url(r'^activate/(?P<activation_key>\w+)/$', views.registration_activate,
        name='registration_activate'),
    url(r'^register/complete/$', views.registration_complete,
        name='registration_complete'),
    url(r'^register/closed/$', views.registration_disallowed,
        name='registration_disallowed'),
]

urlpatterns += [
    url(r'^login/$', decorators.not_auth_required(auth.login),
        {'template_name': 'registration/login.html'}, name='auth_login'),
    url(r'^logout/$', auth.logout,
        {'template_name': 'registration/logout.html'}, name='auth_logout'),
    url(r'^password/change/$', auth.password_change, name='password_change'),
    url(r'^password/change/done/$', auth.password_change_done,
        name='password_change_done'),
    url(r'^password/reset/$', auth.password_reset, name='password_reset'),
    url(r'^password/reset/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        auth.password_reset_confirm, name='password_reset_confirm'),
    url(r'^password/reset/complete/$', auth.password_reset_complete,
        name='password_reset_complete'),
    url(r'^password/reset/done/$', auth.password_reset_done,
        name='password_reset_done'),
]
