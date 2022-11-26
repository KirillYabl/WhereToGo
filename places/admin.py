from adminsortable2.admin import SortableAdminBase
from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.utils.html import format_html

from . import models


class PlaceImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = models.PlaceImage

    readonly_fields = ['image']
    fields = ['place_image', 'image', 'image_order']
    extra = 0

    def image(self, obj):
        return format_html('<img src="{url}" height={height} style="max-height: 200px" />',
                           url=obj.place_image.url,
                           height=obj.place_image.height,
                           )


# Register your models here.
@admin.register(models.Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [PlaceImageInline, ]


@admin.register(models.PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    pass
