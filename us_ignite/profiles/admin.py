from django.contrib import admin

from us_ignite.profiles.models import Profile, ProfileLink

email = lambda u: u.user.email
email.short_description = 'email'


class ProfileLinkInline(admin.TabularInline):
    model = ProfileLink


class ProfileAdmin(admin.ModelAdmin):
    list_display = (email, 'slug')
    search_fields = ('user__first_name', 'slug')
    inlines = [ProfileLinkInline]


admin.site.register(Profile, ProfileAdmin)
