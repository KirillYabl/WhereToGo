from adminsortable2.admin import SortableAdminBase
from adminsortable2.admin import SortableInlineAdminMixin
from django.contrib import admin
from django.utils.html import format_html

from . import models


class PlaceImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = models.PlaceImage

    readonly_fields = ["image"]
    fields = ['place_image', 'image', 'image_order']
    extra = 0

    def image(self, obj):
        max_height = 200
        height = obj.place_image.height
        width = obj.place_image.width
        if height > max_height:
            height_divider = height / max_height
            height = int(height / height_divider)
            width = int(width / height_divider)
        return format_html('<img src="{url}" width="{width}" height={height} />'.format(
            url=obj.place_image.url,
            width=width,
            height=height,
        )
        )


# Register your models here.
@admin.register(models.Place)
class PlaceAdmin(SortableAdminBase, admin.ModelAdmin):
    inlines = [PlaceImageInline, ]


@admin.register(models.PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    pass
