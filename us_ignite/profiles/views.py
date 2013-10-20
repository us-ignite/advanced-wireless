import uuid

from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.contrib.sites.models import RequestSite
from django.shortcuts import render, redirect
from django.views.generic.base import TemplateView

from registration import signals
from registration.backends.default import views as registration_views
from registration.models import RegistrationProfile

from us_ignite.profiles import forms
from us_ignite.profiles.models import Profile


def get_uuid():
    """Removing the reduced size bytes to reduce the risk of collisions.

    More: http://en.wikipedia.org/wiki/Universally_unique_identifier
    #Version_4_.28random.29"""
    stream = uuid.uuid4().hex
    return stream[:12] + stream[13:16] + stream[17:]


class EmailRegistrationView(registration_views.RegistrationView):
    form_class = forms.UserRegistrationForm

    def register(self, request, **cleaned_data):
        """
        Given a username, email address and password, register a new
        user account, which will initially be inactive.

        Along with the new ``User`` object, a new
        ``registration.models.RegistrationProfile`` will be created,
        tied to that ``User``, containing the activation key which
        will be used for this account.

        An email will be sent to the supplied email address; this
        email should contain an activation link. The email will be
        rendered using two templates. See the documentation for
        ``RegistrationProfile.send_activation_email()`` for
        information about these templates and the contexts provided to
        them.

        After the ``User`` and ``RegistrationProfile`` are created and
        the activation email is sent, the signal
        ``registration.signals.user_registered`` will be sent, with
        the new ``User`` as the keyword argument ``user`` and the
        class of this backend as the sender.

        """
        email, password = cleaned_data['email'], cleaned_data['password1']
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)
    # Generate a random username, email is used for login:
        username = get_uuid()
        new_user = (RegistrationProfile.objects
                    .create_inactive_user(username, email, password, site))
        signals.user_registered.send(
            sender=self.__class__, user=new_user, request=request)
        return new_user


# Registration views:
# Using function aliases for lazy loadind and readability in the urls file.
registration_view = EmailRegistrationView.as_view()
registration_activation_complete = TemplateView.as_view(
    template_name='registration/activation_complete.html')
registration_activate = registration_views.ActivationView.as_view()
registration_complete = TemplateView.as_view(
    template_name='registration/registration_complete.html')
registration_disallowed = TemplateView.as_view(
    template_name='registration/registration_closed.html')


@login_required
def user_profile(request):
    """View for the ``Profile`` of the ``User``."""
    # Make sure the user has a profile:
    profile, is_new = Profile.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        form = forms.ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            request.user.first_name = form.cleaned_data['first_name']
            request.user.last_name = form.cleaned_data['last_name']
            request.user.save()
            return redirect('user_profile')
    else:
        form = forms.ProfileForm(instance=profile, initial={
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
        })
    context = {
        'form': form,
    }
    return render(request, 'profile/user_profile.html', context)
