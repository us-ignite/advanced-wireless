from django.contrib import admin

from us_ignite.organizations.models import Organization, OrganizationMember


class OrganizationMembershipInline(admin.TabularInline):
    raw_id_fields = ('user', )
    model = OrganizationMember


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'status', 'created')
    search_fields = ('name', 'slug', 'bio')
    list_filter = ('status', )
    date_hierarchy = 'created'
    inlines = [OrganizationMembershipInline]
    prepopulated_fields = {"slug": ("name",)}


admin.site.register(Organization, OrganizationAdmin)
