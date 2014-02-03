from django.contrib import admin

from us_ignite.maps.models import Category, Location


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'image')
    prepopulated_fields = {"slug": ("name",)}


class LocationAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'category')
    search_fields = ('name', 'website', )
    list_filter = ('status', 'category__name')
    date_hierarchy = 'created'

admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
