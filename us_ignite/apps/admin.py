from django.contrib import admin
from django.conf.urls import patterns, url
from django.template.response import TemplateResponse
from django.shortcuts import redirect

from us_ignite.apps import importer
from us_ignite.apps.forms import ImportForm
from us_ignite.apps.models import (Application, ApplicationURL,
                                   ApplicationMedia, Domain, Feature,
                                   Page, PageApplication)


class ApplicationURLInline(admin.TabularInline):
    model = ApplicationURL


class ApplicationMediaInline(admin.TabularInline):
    model = ApplicationMedia


class ApplicationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'stage', 'status')
    search_fields = ['name', 'slug', 'summary', 'impact_statement',
                     'description', 'roadmap', 'assistance',
                     'team_description', 'notes', 'acknowledgments']
    list_filter = ['stage', 'domain__name', 'status', 'created', ]
    date_hierarchy = 'created'
    inlines = [ApplicationURLInline, ApplicationMediaInline]

    def get_urls(self):
        _import_apps = self.admin_site.admin_view(self.import_apps)
        urls = patterns(
            '',
            url(r'^import/$', _import_apps, name='import_apps'),
        )
        return urls + super(ApplicationAdmin, self).get_urls()

    def import_apps(self, request):
        if request.method == 'POST':
            form = ImportForm(request.POST, request.FILES)
            if form.is_valid():
                result = importer.digest_payload(form.cleaned_data['json'])
                message = '%s apps have been imported.' % len(result)
                self.message_user(request, message)
                return redirect('admin:apps_application_changelist')
        else:
            form = ImportForm()
        context = {'form': form}
        return TemplateResponse(request, 'admin/apps/import.html', context)


class DomainAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')


class PageApplicationInline(admin.TabularInline):
    raw_id_fields = ('application', )
    model = PageApplication


class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'status', 'created', )
    list_filter = ('status', 'created', )
    date_hierarchy = 'created'
    inlines = [PageApplicationInline]

admin.site.register(Application, ApplicationAdmin)
admin.site.register(Domain, DomainAdmin)
admin.site.register(Feature, FeatureAdmin)
admin.site.register(Page, PageAdmin)
