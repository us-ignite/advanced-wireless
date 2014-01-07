from django.contrib import admin

from us_ignite.uploads.models import Image, Upload


class ImageAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', )


class UploadAdmin(admin.ModelAdmin):
    list_display = ('title', 'attachment', )


admin.site.register(Image, ImageAdmin)
admin.site.register(Upload, UploadAdmin)
