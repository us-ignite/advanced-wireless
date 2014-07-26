from django import forms
from django.contrib import admin
from django.contrib.redirects.models import Redirect
from django.contrib.sites.models import get_current_site


admin.site.unregister(Redirect)


class RedirectAdminForm(forms.ModelForm):
    class Meta:
        model = Redirect
        fields = ('old_path', 'new_path')


class RedirectAdmin(admin.ModelAdmin):
    form = RedirectAdminForm

    def save_model(self, request, obj, form, change):
        obj.site = get_current_site(request)
        obj.save()


admin.site.register(Redirect, RedirectAdmin)
