from django.contrib import admin

from us_ignite.maps.models import Category, Location


class CategoryAdmin(admin.ModelAdmin):
    pass


class LocationAdmin(admin.ModelAdmin):
    pass

admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
