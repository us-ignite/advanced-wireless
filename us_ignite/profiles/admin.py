from django.contrib import admin

from us_ignite.profiles.models import Profile, ProfileLink

email = lambda u: u.user.email
email.short_description = 'email'


class ProfileAdmin(admin.ModelAdmin):
    list_display = (email, 'slug')
    search_fields = ('user__first_name', 'slug')


admin.site.register(Profile, ProfileAdmin)
admin.site.register([ProfileLink])
