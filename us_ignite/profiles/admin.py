from django.contrib import admin
from django.conf.urls import patterns, url
from django.shortcuts import render, redirect

from us_ignite.profiles.models import Profile, ProfileLink
from us_ignite.profiles import inviter, forms


email = lambda u: u.user.email
email.short_description = 'email'


class ProfileLinkInline(admin.TabularInline):
    model = ProfileLink


class ProfileAdmin(admin.ModelAdmin):
    list_display = (email, 'display_name', 'slug')
    search_fields = ('user__first_name', 'slug', 'display_name')
    inlines = [ProfileLinkInline]

    def get_urls(self):
        _invite_users = self.admin_site.admin_view(self.invite_users)
        urls = patterns(
            '',
            url(r'^inviter/$', _invite_users, name='invite_users'),
        )
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


admin.site.register(Profile, ProfileAdmin)
