from django.contrib import admin
from django.conf.urls import patterns, url
from django.shortcuts import redirect
from django.http import Http404
from django.template.response import TemplateResponse

from us_ignite.actionclusters.forms import ActionClusterApprovalRequestForm
from us_ignite.actionclusters.models import ActionCluster, ActionClusterRequest

def get_actioncluster_from_request(instance):
    """Transform the instance in a request"""
    return ActionCluster.objects.create(
        name=instance.name,
        contact=instance.user,
        summary=instance.summary,
        description=instance.description,
        website=instance.website
    )

class ActionClusterAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created')
    search_fields = ('name', 'description', 'summary')
    date_hierarchy = 'created'
    list_filter = ('status', )

class ActionClusterRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created')
    search_fields = ('name', 'description')
    date_hierarchy = 'created'
    list_filter = ('status', 'created')

    def get_urls(self):
        _approve_request = self.admin_site.admin_view(self.approve_request)
        urls = patterns(
            '',
            url(r'^approve/(?P<request_id>\d+)/$', _approve_request,
                name='approve_hub_request')
        )
        urls += super(ActionClusterRequestAdmin, self).get_urls()
        return urls

    def approve_request(self, request, request_id):
        """Aprove the user request to own a community."""
        try:
            instance = ActionClusterRequest.objects.get(id=request_id)
        except ActionClusterRequest.DoesNotExist:
            raise Http404
        # Determine if this request has been processed:
        if not instance.is_pending():
            raise Http404
        if request.method == 'POST':
            form = ActionClusterApprovalRequestForm(request.POST, instance=instance)
            if form.is_valid():
                instance = form.save()
                # Process the request approval.
                if instance.is_approved():
                    actioncluster = get_actioncluster_from_request(instance)
                    instance.actioncluster = actioncluster
                    instance.save()
                self.message_user(request, 'Action cluster request has been updated.')
                return redirect(
                    'admin:actionclusters_actionclusterrequest_change', request_id)
        else:
            form = ActionClusterApprovalRequestForm(instance=instance)
        context = {
            'object': instance,
            'form': form,
            'title': 'Resolve Ignite community request',
        }
        return TemplateResponse(
            request, 'admin/hubs/request_approval.html', context)

admin.site.register(ActionCluster, ActionClusterAdmin)
admin.site.register(ActionClusterRequest, ActionClusterRequestAdmin)