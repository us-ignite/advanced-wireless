from django.contrib import admin
from django.conf.urls import *
from django.shortcuts import redirect
from django.http import Http404
from django.template.response import TemplateResponse

from us_ignite.hubs.forms import HubApprovalRequestForm
from us_ignite.hubs.models import Hub, HubRequest, HubURL


def get_hub_from_request(instance):
    """Transform the instance in a request"""
    return Hub.objects.create(
        name=instance.name,
        contact=instance.user,
        summary=instance.summary,
        description=instance.description,
        website=instance.website
    )


class HubRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created')
    search_fields = ('name', 'description')
    date_hierarchy = 'created'
    list_filter = ('status', 'created')

    def get_urls(self):
        _approve_request = self.admin_site.admin_view(self.approve_request)
        urls = [
            url(r'^approve/(?P<request_id>\d+)/$', _approve_request,
                name='approve_hub_request')
        ]
        urls += super(HubRequestAdmin, self).get_urls()
        return urls

    def approve_request(self, request, request_id):
        """Aprove the user request to own a community."""
        try:
            instance = HubRequest.objects.get(id=request_id)
        except HubRequest.DoesNotExist:
            raise Http404
        # Determine if this request has been processed:
        if not instance.is_pending():
            raise Http404
        if request.method == 'POST':
            form = HubApprovalRequestForm(request.POST, instance=instance)
            if form.is_valid():
                instance = form.save()
                # Process the request approval.
                if instance.is_approved():
                    hub = get_hub_from_request(instance)
                    instance.hub = hub
                    instance.save()
                self.message_user(request, 'Hub request has been updated.')
                return redirect(
                    'admin:hubs_hubrequest_change', request_id)
        else:
            form = HubApprovalRequestForm(instance=instance)
        context = {
            'object': instance,
            'form': form,
            'title': 'Resolve Ignite community request',
        }
        return TemplateResponse(
            request, 'admin/hubs/request_approval.html', context)


class HubURLInline(admin.TabularInline):
    model = HubURL


class HubAdmin(admin.ModelAdmin):
    raw_id_fields = ('contact', )
    list_display = ('name', 'slug', 'status', 'created')
    search_fields = ('name', 'slug', 'description', 'summary')
    date_hierarchy = 'created'
    list_filter = ('status', 'created')
    inlines = [HubURLInline]

admin.site.register(Hub, HubAdmin)
admin.site.register(HubRequest, HubRequestAdmin)
