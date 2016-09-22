from django.utils import timezone
from django.contrib import admin
from django.conf.urls import *
from django.shortcuts import render, redirect

from us_ignite.profiles.models import Profile, ProfileLink
from us_ignite.profiles import exporter, forms, inviter


email = lambda u: u.user.email
email.short_description = 'email'


def _get_filename(name):
    return '%s-%s' % (name, timezone.now().strftime("%Y%m%dT%H%M%S"))


class ProfileLinkInline(admin.TabularInline):
    model = ProfileLink


class ProfileAdmin(admin.ModelAdmin):
    list_display = (email, 'user', 'slug')
    search_fields = ('user__first_name', 'slug', 'user__last_name')
    inlines = [ProfileLinkInline]

    def get_urls(self):
        _invite_users = self.admin_site.admin_view(self.invite_users)
        _export_users = self.admin_site.admin_view(self.export_users)
        urls = [
            url(r'^inviter/$', _invite_users, name='invite_users'),
            url(r'^export/$', _export_users, name='export_users'),
        ]
        urls += super(ProfileAdmin, self).get_urls()
        return urls

    def _notify_results(self, request, results):
        if results:
            message = '%s users were imported correctly.' % len(results)
        else:
            message = 'No new users were imported.'
        self.message_user(request, message)

    def invite_users(self, request):
        """Invites a list of provided users.

        Each new user should be in a different line and the format
        of each row is::

            name, email
        """
        if request.method == 'POST':
            form = forms.InviterForm(request.POST)
            if form.is_valid():
                results = inviter.invite_users(form.cleaned_data['users'])
                self._notify_results(request, results)
                return redirect('admin:profiles_profile_changelist')
        else:
            form = forms.InviterForm()
        context = {
            'form': form,
            'title': 'Invite users',
        }
        return render(request, 'admin/profiles/inviter.html', context)

    def export_users(self, request):
        """Generate a CSV file with the existing user Profiles.

        Since users without a profile are not considered by using
        the Profile creation date the app guarantees that the sooner
        or later the user will be returned."""
        if request.method == 'POST':
            form = forms.UserExportForm(request.POST)
            if form.is_valid():
                kwargs = {}
                filename = 'US-Ignite-Users'
                start = form.cleaned_data.get('start')
                if start:
                    kwargs['created__gte'] = start
                    filename += '-from-%s' % start.strftime("%d%b%y")
                end = form.cleaned_data.get('end')
                if end:
                    kwargs['created__lte'] = end
                    filename += '-until-%s' % end.strftime("%d%b%y")
                user_qs = Profile.active.filter(**kwargs)
                if user_qs:
                    filename = _get_filename(filename)
                    user_list = exporter.export_users(user_qs)
                    return exporter.csv_response(filename, user_list)
                self.message_user(
                    request, 'No users registered during the given dates.')
        else:
            form = forms.UserExportForm()
        context = {
            'form': form,
            'title': 'Export users',
        }
        return render(request, 'admin/profiles/export.html', context)


admin.site.register(Profile, ProfileAdmin)
